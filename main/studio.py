import json
import time

from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Count, Q, Sum
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from lessons.models import Attempt, Course, CourseModule, Exercise

from .models import Lesson, Progress, Quest, Submission, World


def _is_staff(user):
    return user.is_active and user.is_staff


studio_staff_required = user_passes_test(_is_staff, login_url='main:studio_login')

LOGIN_LIMIT_COUNT = 5
LOGIN_LOCK_SECONDS = 10 * 60


class StudioJSONWidget(forms.Textarea):
    """Textarea that keeps JSON readable in the custom studio forms."""

    def format_value(self, value):
        if value in (None, ''):
            return ''
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return value
        return json.dumps(value, ensure_ascii=False, indent=2)


class StudioModelForm(forms.ModelForm):
    """Base form with frontend-friendly widgets for all studio models."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'studio-input')
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'studio-checkbox'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'studio-select'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('rows', 7)
                field.widget.attrs['class'] = 'studio-textarea'
            elif name in {'color', 'accent'}:
                field.widget = forms.TextInput(attrs={'class': 'studio-input studio-color', 'type': 'color'})

    @classmethod
    def formfield_callback(cls, db_field, **kwargs):
        if db_field.get_internal_type() == 'JSONField':
            kwargs['widget'] = StudioJSONWidget(attrs={'class': 'studio-textarea studio-code', 'rows': 10})
        return db_field.formfield(**kwargs)


class StudioLoginForm(AuthenticationForm):
    """Only active staff accounts can authenticate into Studio."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'not_staff': 'У этой учетной записи нет доступа к админ-панели.',
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages['not_staff'],
                code='not_staff',
            )


def _status(value, good='На сайте', bad='Скрыто'):
    tone = 'good' if value else 'muted'
    label = good if value else bad
    return format_html('<span class="studio-pill {}">{}</span>', tone, label)


def _result(value):
    tone = 'good' if value else 'danger'
    label = 'Решено' if value else 'Ошибка'
    return format_html('<span class="studio-pill {}">{}</span>', tone, label)


def _difficulty(obj):
    tones = {1: 'good', 2: 'warn', 3: 'danger'}
    label = obj.get_difficulty_display()
    return format_html('<span class="studio-pill {}">{}</span>', tones.get(obj.difficulty, 'muted'), label)


def _score(obj):
    return f'{obj.passed_tests}/{obj.total_tests}'


MODEL_CONFIG = {
    'worlds': {
        'model': World,
        'title': 'Научные миры',
        'singular': 'мир',
        'section': 'EduQuest',
        'icon': '🌐',
        'search': ('title', 'subject', 'intro'),
        'columns': (
            ('title', 'Название'),
            ('subject', 'Предмет'),
            ('lessons_count', 'Уроки'),
            ('quests_count', 'Квесты'),
            ('order', 'Порядок'),
        ),
        'annotate': lambda qs: qs.annotate(lessons_count=Count('lessons'), quests_count=Count('quests')),
        'editable': True,
    },
    'lessons': {
        'model': Lesson,
        'title': 'Уроки',
        'singular': 'урок',
        'section': 'EduQuest',
        'icon': '📚',
        'search': ('title', 'intro', 'theme', 'world__title'),
        'columns': (
            ('title', 'Название'),
            ('world', 'Мир'),
            ('theme', 'Тема'),
            ('steps_count', 'Шаги'),
            ('is_active', 'Статус', lambda obj: _status(obj.is_active, 'Опубликован', 'Скрыт')),
        ),
        'annotate': lambda qs: qs.select_related('world').annotate(steps_count=Count('steps')),
        'editable': True,
    },
    'quests': {
        'model': Quest,
        'title': 'Квесты',
        'singular': 'квест',
        'section': 'EduQuest',
        'icon': '🧪',
        'search': ('title', 'story', 'theory', 'world__title', 'lesson__title'),
        'columns': (
            ('title', 'Название'),
            ('world', 'Мир'),
            ('lesson', 'Урок'),
            ('task_type', 'Тип', lambda obj: obj.get_task_type_display()),
            ('difficulty', 'Сложность', _difficulty),
            ('is_active', 'Статус', lambda obj: _status(obj.is_active, 'На сайте', 'Скрыт')),
        ),
        'annotate': lambda qs: qs.select_related('world', 'lesson'),
        'editable': True,
    },
    'courses': {
        'model': Course,
        'title': 'Курсы',
        'singular': 'курс',
        'section': 'PyTeacher',
        'icon': '🎓',
        'search': ('title', 'description'),
        'columns': (
            ('title', 'Название'),
            ('slug', 'URL'),
            ('modules_count', 'Модули'),
            ('is_active', 'Статус', lambda obj: _status(obj.is_active, 'Активен', 'Скрыт')),
        ),
        'annotate': lambda qs: qs.annotate(modules_count=Count('modules')),
        'editable': True,
    },
    'modules': {
        'model': CourseModule,
        'title': 'Модули',
        'singular': 'модуль',
        'section': 'PyTeacher',
        'icon': '🧩',
        'search': ('title', 'description', 'course__title'),
        'columns': (
            ('title', 'Название'),
            ('course', 'Курс'),
            ('exercises_count', 'Задачи'),
            ('order', 'Порядок'),
        ),
        'annotate': lambda qs: qs.select_related('course').annotate(exercises_count=Count('exercises')),
        'editable': True,
    },
    'exercises': {
        'model': Exercise,
        'title': 'Задачи Python',
        'singular': 'задачу',
        'section': 'PyTeacher',
        'icon': '💻',
        'search': ('title', 'topic', 'task_text', 'module__title'),
        'columns': (
            ('title', 'Название'),
            ('module', 'Модуль'),
            ('topic', 'Тема'),
            ('difficulty', 'Сложность', _difficulty),
            ('is_active', 'Статус', lambda obj: _status(obj.is_active, 'На сайте', 'Скрыта')),
        ),
        'annotate': lambda qs: qs.select_related('module', 'module__course'),
        'editable': True,
    },
    'submissions': {
        'model': Submission,
        'title': 'Отправки квестов',
        'singular': 'отправку',
        'section': 'История',
        'icon': '📈',
        'search': ('session_key', 'quest__title', 'feedback'),
        'columns': (
            ('quest', 'Квест'),
            ('session_key', 'Сессия'),
            ('is_success', 'Результат', lambda obj: _result(obj.is_success)),
            ('score', 'Тесты', _score),
            ('created_at', 'Дата'),
        ),
        'annotate': lambda qs: qs.select_related('quest', 'quest__world'),
        'editable': False,
    },
    'attempts': {
        'model': Attempt,
        'title': 'Попытки Python',
        'singular': 'попытку',
        'section': 'История',
        'icon': '🧾',
        'search': ('session_key', 'exercise__title', 'feedback'),
        'columns': (
            ('exercise', 'Задача'),
            ('session_key', 'Сессия'),
            ('is_success', 'Результат', lambda obj: _result(obj.is_success)),
            ('score', 'Тесты', _score),
            ('created_at', 'Дата'),
        ),
        'annotate': lambda qs: qs.select_related('exercise'),
        'editable': False,
    },
    'progress': {
        'model': Progress,
        'title': 'Прогресс',
        'singular': 'прогресс',
        'section': 'История',
        'icon': '🏁',
        'search': ('session_key', 'world__title'),
        'columns': (
            ('session_key', 'Сессия'),
            ('world', 'Мир'),
            ('points', 'RP'),
            ('solved_count', 'Решено'),
            ('updated_at', 'Обновлено'),
        ),
        'annotate': lambda qs: qs.select_related('world'),
        'editable': False,
    },
}


def _get_config(model_key):
    try:
        return MODEL_CONFIG[model_key]
    except KeyError as exc:
        raise Http404('Раздел студии не найден.') from exc


def _nav_groups():
    groups = {}
    for key, config in MODEL_CONFIG.items():
        groups.setdefault(config['section'], []).append({'key': key, **config})
    return groups


def _apply_search(queryset, config, query):
    if not query:
        return queryset
    condition = Q()
    for field in config['search']:
        condition |= Q(**{f'{field}__icontains': query})
    return queryset.filter(condition)


def _row_cells(obj, config):
    cells = []
    for column in config['columns']:
        field_name, label = column[:2]
        renderer = column[2] if len(column) > 2 else None
        value = renderer(obj) if renderer else getattr(obj, field_name)
        cells.append({'name': field_name, 'label': label, 'value': value})
    return cells


def _model_form(model):
    readonly_fields = {'id'}
    fields = [
        field.name
        for field in model._meta.fields
        if field.name not in readonly_fields and not getattr(field, 'auto_now', False) and not getattr(field, 'auto_now_add', False)
    ]
    return modelform_factory(
        model,
        form=StudioModelForm,
        fields=fields,
        formfield_callback=StudioModelForm.formfield_callback,
    )


def _field_groups(form):
    groups = [
        ('Основное', []),
        ('Контент', []),
        ('Проверка', []),
        ('Публикация', []),
    ]
    content_names = {'intro', 'description', 'story', 'theory', 'hint', 'easier_text', 'task_text', 'short_description'}
    check_names = {'starter_code', 'tests', 'content', 'code', 'feedback'}
    publish_names = {'slug', 'order', 'step_order', 'reward_points', 'min_points_required', 'is_active', 'color', 'accent', 'icon', 'visual_kind'}
    for field in form:
        target = groups[0][1]
        if field.name in content_names:
            target = groups[1][1]
        elif field.name in check_names:
            target = groups[2][1]
        elif field.name in publish_names:
            target = groups[3][1]
        target.append(field)
    return [group for group in groups if group[1]]


def studio_redirect(request, path=''):
    target = '/admin/'
    if path:
        target += path
    if request.GET:
        target += f'?{request.GET.urlencode()}'
    return redirect(target)


def _login_attempt_state(request):
    return request.session.get('studio_login_attempts', {'count': 0, 'locked_until': 0})


def _remember_failed_login(request):
    state = _login_attempt_state(request)
    state['count'] = int(state.get('count', 0)) + 1
    if state['count'] >= LOGIN_LIMIT_COUNT:
        state['locked_until'] = int(time.time()) + LOGIN_LOCK_SECONDS
    request.session['studio_login_attempts'] = state


def _clear_failed_logins(request):
    request.session.pop('studio_login_attempts', None)


@sensitive_post_parameters('password')
@csrf_protect
@never_cache
def studio_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('main:studio_dashboard')

    form = StudioLoginForm(request, data=request.POST or None)
    state = _login_attempt_state(request)
    locked_until = int(state.get('locked_until', 0))
    is_locked = locked_until > int(time.time())

    if request.method == 'POST':
        if is_locked:
            minutes = max(round((locked_until - int(time.time())) / 60), 1)
            form.add_error(None, f'Слишком много попыток входа. Попробуйте через {minutes} мин.')
        elif form.is_valid():
            _clear_failed_logins(request)
            login(request, form.get_user())
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('main:studio_dashboard')
        else:
            _remember_failed_login(request)

    return render(request, 'studio/login.html', {'form': form})


@csrf_protect
@never_cache
def studio_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('main:studio_login')


@studio_staff_required
def studio_dashboard(request):
    worlds = World.objects.count()
    lessons = Lesson.objects.count()
    quests = Quest.objects.count()
    exercises = Exercise.objects.count()
    solved_submissions = Submission.objects.filter(is_success=True).count()
    total_points = Progress.objects.aggregate(total=Sum('points'))['total'] or 0
    recent_submissions = Submission.objects.select_related('quest', 'quest__world')[:6]
    recent_attempts = Attempt.objects.select_related('exercise')[:6]

    cards = [
        {'label': 'Миры', 'value': worlds, 'url': reverse('main:studio_model_list', args=['worlds'])},
        {'label': 'Уроки', 'value': lessons, 'url': reverse('main:studio_model_list', args=['lessons'])},
        {'label': 'Квесты', 'value': quests, 'url': reverse('main:studio_model_list', args=['quests'])},
        {'label': 'Python-задачи', 'value': exercises, 'url': reverse('main:studio_model_list', args=['exercises'])},
        {'label': 'Успешных решений', 'value': solved_submissions, 'url': reverse('main:studio_model_list', args=['submissions'])},
        {'label': 'Всего RP', 'value': total_points, 'url': reverse('main:studio_model_list', args=['progress'])},
    ]
    return render(
        request,
        'studio/dashboard.html',
        {
            'nav_groups': _nav_groups(),
            'cards': cards,
            'recent_submissions': recent_submissions,
            'recent_attempts': recent_attempts,
            'active_key': 'dashboard',
        },
    )


@studio_staff_required
def studio_model_list(request, model_key):
    config = _get_config(model_key)
    queryset = config['model'].objects.all()
    queryset = config.get('annotate', lambda qs: qs)(queryset)
    query = request.GET.get('q', '').strip()
    queryset = _apply_search(queryset, config, query)
    objects = list(queryset[:100])
    rows = [{'object': obj, 'cells': _row_cells(obj, config)} for obj in objects]
    return render(
        request,
        'studio/model_list.html',
        {
            'nav_groups': _nav_groups(),
            'active_key': model_key,
            'config': config,
            'model_key': model_key,
            'query': query,
            'rows': rows,
            'total_count': queryset.count(),
        },
    )


@studio_staff_required
def studio_model_create(request, model_key):
    config = _get_config(model_key)
    if not config['editable']:
        messages.error(request, 'Эта сущность доступна только для просмотра.')
        return redirect('main:studio_model_list', model_key=model_key)

    FormClass = _model_form(config['model'])
    form = FormClass(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        messages.success(request, f'{config["singular"].capitalize()} сохранен.')
        return redirect('main:studio_model_edit', model_key=model_key, pk=obj.pk)

    return render(
        request,
        'studio/model_form.html',
        {
            'nav_groups': _nav_groups(),
            'active_key': model_key,
            'config': config,
            'model_key': model_key,
            'form': form,
            'field_groups': _field_groups(form),
            'object': None,
            'mode': 'create',
        },
    )


@studio_staff_required
def studio_model_edit(request, model_key, pk):
    config = _get_config(model_key)
    obj = get_object_or_404(config['model'], pk=pk)
    if not config['editable']:
        messages.info(request, 'Эта запись открыта в режиме просмотра.')

    FormClass = _model_form(config['model'])
    form = FormClass(request.POST or None, instance=obj)
    if not config['editable']:
        for field in form.fields.values():
            field.disabled = True

    if request.method == 'POST' and config['editable'] and form.is_valid():
        form.save()
        messages.success(request, 'Изменения сохранены.')
        return redirect('main:studio_model_edit', model_key=model_key, pk=obj.pk)

    return render(
        request,
        'studio/model_form.html',
        {
            'nav_groups': _nav_groups(),
            'active_key': model_key,
            'config': config,
            'model_key': model_key,
            'form': form,
            'field_groups': _field_groups(form),
            'object': obj,
            'mode': 'edit' if config['editable'] else 'view',
        },
    )


@studio_staff_required
def studio_model_delete(request, model_key, pk):
    config = _get_config(model_key)
    obj = get_object_or_404(config['model'], pk=pk)
    if not config['editable']:
        messages.error(request, 'Эту сущность нельзя удалить из студии.')
        return redirect('main:studio_model_list', model_key=model_key)

    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Запись удалена.')
        return redirect('main:studio_model_list', model_key=model_key)

    return render(
        request,
        'studio/confirm_delete.html',
        {
            'nav_groups': _nav_groups(),
            'active_key': model_key,
            'config': config,
            'model_key': model_key,
            'object': obj,
        },
    )
