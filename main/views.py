from types import SimpleNamespace
from secrets import token_urlsafe

from django.db.models import Count, Max, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .checker import check_solution
from .forms import CodeSubmissionForm
from .models import Lesson, Progress, Quest, Submission, World
from .textbook_content import TEXTBOOKS


CHEMIST_CAREER = [
    {
        'title': 'Ассистент лаборатории',
        'points': 0,
        'description': 'Учится работать с данными, не боится пробирок и первых ошибок в коде.',
    },
    {
        'title': 'Лаборант-аналитик',
        'points': 60,
        'description': 'Уверенно проходит тесты и начинает видеть связь между формулами и Python.',
    },
    {
        'title': 'Младший химик',
        'points': 140,
        'description': 'Пишет расчеты для реактора, проверяет гипотезы и собирает учебные данные.',
    },
    {
        'title': 'Инженер реактора',
        'points': 260,
        'description': 'Умеет превращать задачи по химии, биологии и географии в понятные алгоритмы.',
    },
    {
        'title': 'Руководитель научной группы',
        'points': 420,
        'description': 'Ведет исследовательский проект и открывает самые сложные сценарии платформы.',
    },
]


CHEMIST_UPGRADES = [
    {
        'id': 'coat',
        'title': 'Лабораторный халат',
        'points': 30,
        'effect': '+ уверенность в первых опытах',
        'description': 'Базовое улучшение персонажа. Показывает, что ученик сделал первые шаги.',
    },
    {
        'id': 'notebook',
        'title': 'Полевой блокнот',
        'points': 80,
        'effect': '+ системность в решениях',
        'description': 'Помогает связывать теорию, условия задач и код в одну цепочку.',
    },
    {
        'id': 'reactor',
        'title': 'Мини-реактор',
        'points': 160,
        'effect': '+ расчеты по химии',
        'description': 'Символ того, что ученик уже готов к задачам с формулами и процентами.',
    },
    {
        'id': 'microscope',
        'title': 'Цифровой микроскоп',
        'points': 260,
        'effect': '+ анализ биоданных',
        'description': 'Открывает образ исследователя, который умеет работать с клетками и ДНК.',
    },
    {
        'id': 'ai_station',
        'title': 'Станция прогнозов',
        'points': 420,
        'effect': '+ сложные модели',
        'description': 'Финальное улучшение для задач с прогнозами, эволюцией и большими наборами данных.',
    },
]


LEGACY_TEXTBOOKS = [
    {
        'title': 'Python для научных задач',
        'subject': 'Программирование',
        'topics': [
            {
                'name': 'Списки и словари',
                'text': 'Списки удобны для последовательностей измерений, а словари — для пар ключ-значение: элемент и масса, город и температура, вид и численность.',
            },
            {
                'name': 'Функция solve(...)',
                'text': 'Все Python-задачи проверяются через функцию solve. Она получает входные данные из тестов и должна вернуть результат без input и print.',
            },
            {
                'name': 'Округление',
                'text': 'Для процентов и индексов используйте round(value, 2) или round(value, 3), если в условии нужен точный формат ответа.',
            },
        ],
    },
    {
        'title': 'Биология и биоинформатика',
        'subject': 'Биология',
        'topics': [
            {
                'name': 'ДНК и GC-процент',
                'text': 'ДНК записывается буквами A, T, C, G. GC-процент показывает долю G и C среди всех нуклеотидов и помогает сравнивать последовательности.',
            },
            {
                'name': 'Белковые последовательности',
                'text': 'Белки записывают буквами аминокислот. Повторы и мотивы помогают находить участки, которые могут быть важны для структуры или функции белка.',
            },
            {
                'name': 'Индекс Шеннона',
                'text': 'Индекс Шеннона оценивает биоразнообразие: учитывает не только число видов, но и равномерность их распределения в экосистеме.',
            },
        ],
    },
    {
        'title': 'Химия в расчетах',
        'subject': 'Химия',
        'topics': [
            {
                'name': 'Молярная масса',
                'text': 'Молярная масса вещества складывается из атомных масс элементов с учетом количества атомов в формуле.',
            },
            {
                'name': 'Массовая доля',
                'text': 'Массовая доля показывает, какую часть общей массы составляет элемент или вещество: часть / целое * 100%.',
            },
            {
                'name': 'Концентрация',
                'text': 'Концентрация помогает понять, сколько вещества находится в растворе. Такие задачи хорошо решаются через функции и словари.',
            },
        ],
    },
    {
        'title': 'География данных',
        'subject': 'География',
        'topics': [
            {
                'name': 'Климатические данные',
                'text': 'Температура, осадки и координаты удобно хранить в списках словарей, чтобы потом фильтровать и считать средние значения.',
            },
            {
                'name': 'Маршруты',
                'text': 'Маршрут можно описать списком точек. Для учебных карт расстояние часто считают как сумму изменений по координатам.',
            },
            {
                'name': 'JSON-формат',
                'text': 'JSON похож на словари и списки Python. Он удобен для обмена структурированными данными между сайтом, сервером и задачами.',
            },
        ],
    },
]


def _session_key(request):
    """Возвращает стабильный учебный ключ без записи в DB-сессии."""

    key = request.session.get('student_key') or request.session.session_key
    if not key:
        key = token_urlsafe(24)
    request.session['student_key'] = key
    return key


def _progress_for_world(session_key, world):
    """Returns saved progress or a zero-value object without writing on GET."""

    return Progress.objects.filter(session_key=session_key, world=world).first() or SimpleNamespace(
        world=world,
        points=0,
        solved_count=0,
    )


def _student_summary(session_key):
    """Собирает общий уровень, баллы и достижения ученика."""

    total_points = Progress.objects.filter(session_key=session_key).aggregate(
        total=Sum('points')
    )['total'] or 0
    solved = Submission.objects.filter(session_key=session_key, is_success=True).values(
        'quest_id'
    ).distinct().count()

    achievements = []
    if solved >= 1:
        achievements.append('Первый квест')
    if solved >= 3:
        achievements.append('Полевой исследователь')
    if total_points >= 120:
        achievements.append('Научный навигатор')

    knowledge_tree = ['Переменные и типы данных']
    if total_points >= 40:
        knowledge_tree.append('Циклы и условия')
    if total_points >= 90:
        knowledge_tree.append('Списки и словари')
    if total_points >= 160:
        knowledge_tree.append('Алгоритмы анализа данных')
    if total_points >= 260:
        knowledge_tree.append('Проектное мышление и ООП')

    level = 'Новичок'
    if total_points >= 140:
        level = 'Эксперт'
    elif total_points >= 60:
        level = 'Исследователь'

    return {
        'total_points': total_points,
        'solved': solved,
        'level': level,
        'achievements': achievements,
        'knowledge_tree': knowledge_tree,
        'evolution_stage': min(total_points // 80, 3),
    }


def _get_textbook(book_slug):
    """Ищет учебник по slug-у из статического справочника."""

    for book in TEXTBOOKS:
        if book['slug'] == book_slug:
            return book
    raise Http404('Учебник не найден.')


def _get_textbook_topic(book, topic_slug):
    """Ищет тему внутри выбранного учебника."""

    for topic in book['topics']:
        if topic['slug'] == topic_slug:
            return topic
    raise Http404('Тема учебника не найдена.')


def _check_non_python_answer(quest, request):
    """Проверяет тест или сопоставление без запуска Python-кода.

    Для таких заданий правильные ответы лежат в quest.content. Это проще для
    учителя: можно добавить предметное задание через админку и не писать код.
    """

    if quest.task_type == Quest.TaskType.QUIZ:
        selected = request.POST.get('answer', '')
        correct = quest.content.get('correct')
        is_success = selected == correct
        feedback = 'Верно: предметная часть квеста закрыта.' if is_success else 'Пока нет. Перечитайте справку и попробуйте еще раз.'
        return selected, is_success, int(is_success), 1, feedback

    if quest.task_type == Quest.TaskType.MATCH:
        pairs = quest.content.get('pairs', [])
        total = len(pairs)
        passed = 0
        answers = {}
        for index, pair in enumerate(pairs):
            field = f'match_{index}'
            selected = request.POST.get(field, '')
            answers[field] = selected
            if selected == pair.get('answer'):
                passed += 1

        is_success = total > 0 and passed == total
        feedback = 'Все пары собраны правильно.' if is_success else f'Правильно сопоставлено: {passed}/{total}.'
        return str(answers), is_success, passed, total, feedback

    return '', False, 0, 1, 'Неизвестный тип задания.'


def _save_success_progress(session_key, quest):
    """Начисляет баллы только за первое успешное решение квеста."""

    progress, _ = Progress.objects.get_or_create(session_key=session_key, world=quest.world)
    progress.points += quest.reward_points
    progress.solved_count += 1
    progress.save()


def _chemist_state(session_key, active_upgrade_ids):
    """Собирает состояние игрового персонажа без отдельной таблицы в базе.

    Карьера химика зависит от общего учебного прогресса, а улучшения хранятся в
    сессии браузера. Такой подход прост для учебного проекта и не ломает текущие модели.
    """

    summary = _student_summary(session_key)
    total_points = summary['total_points']
    solved = summary['solved']
    chemistry = World.objects.filter(slug='chemistry').first()
    chemistry_progress = None
    if chemistry:
        chemistry_progress = Progress.objects.filter(
            session_key=session_key,
            world=chemistry,
        ).first()

    current_stage = CHEMIST_CAREER[0]
    next_stage = None
    for index, stage in enumerate(CHEMIST_CAREER):
        if total_points >= stage['points']:
            current_stage = stage
            next_stage = CHEMIST_CAREER[index + 1] if index + 1 < len(CHEMIST_CAREER) else None

    if next_stage:
        previous_points = current_stage['points']
        needed = next_stage['points'] - previous_points
        gained = max(total_points - previous_points, 0)
        career_percent = min(round(gained / needed * 100), 100) if needed else 100
    else:
        career_percent = 100

    upgrades = []
    for upgrade in CHEMIST_UPGRADES:
        is_unlocked = total_points >= upgrade['points']
        upgrades.append({
            **upgrade,
            'is_unlocked': is_unlocked,
            'is_active': upgrade['id'] in active_upgrade_ids,
        })

    active_count = sum(1 for upgrade in upgrades if upgrade['is_active'])
    chemistry_points = chemistry_progress.points if chemistry_progress else 0
    chemistry_solved = chemistry_progress.solved_count if chemistry_progress else 0

    return {
        'summary': summary,
        'current_stage': current_stage,
        'next_stage': next_stage,
        'career_percent': career_percent,
        'upgrades': upgrades,
        'active_count': active_count,
        'chemistry_points': chemistry_points,
        'chemistry_solved': chemistry_solved,
        'solved': solved,
        'total_points': total_points,
    }


def home(request):
    """Главная страница с тремя научными мирами."""

    session_key = _session_key(request)
    worlds = World.objects.annotate(
        quests_count=Count('quests', filter=Q(quests__is_active=True)),
    )
    return render(
        request,
        'main/home.html',
        {
            'worlds': worlds,
            'summary': _student_summary(session_key),
        },
    )


def world_detail(request, slug):
    """Страница мира: интерактивная карта, задачи и визуализация прогресса."""

    session_key = _session_key(request)
    world = get_object_or_404(World, slug=slug)
    lessons = Lesson.objects.filter(world=world, is_active=True).annotate(
        steps_count=Count('steps', filter=Q(steps__is_active=True)),
        solved_steps=Count(
            'steps',
            filter=Q(steps__submissions__session_key=session_key, steps__submissions__is_success=True),
            distinct=True,
        ),
        failed_steps=Count(
            'steps',
            filter=Q(steps__submissions__session_key=session_key, steps__submissions__is_success=False),
            distinct=True,
        ),
    )
    quests = Quest.objects.filter(world=world, is_active=True).annotate(
        solved_at=Max(
            'submissions__created_at',
            filter=Q(submissions__session_key=session_key, submissions__is_success=True),
        ),
        tries=Count('submissions', filter=Q(submissions__session_key=session_key)),
    )
    progress = _progress_for_world(session_key, world)
    lesson_cards = []
    for lesson in lessons:
        lesson_cards.append({
            'lesson': lesson,
            'is_unlocked': progress.points >= lesson.min_points_required,
        })
    lesson_groups = []
    groups_by_title = {}
    for card in lesson_cards:
        theme = card['lesson'].theme or 'Основные темы'
        if theme not in groups_by_title:
            group = {'title': theme, 'lessons': []}
            groups_by_title[theme] = group
            lesson_groups.append(group)
        groups_by_title[theme]['lessons'].append(card)

    return render(
        request,
        'main/world.html',
        {
            'world': world,
            'lessons': lesson_cards,
            'lesson_groups': lesson_groups,
            'quests': quests,
            'progress': progress,
            'summary': _student_summary(session_key),
        },
    )


def lesson_detail(request, world_slug, lesson_slug):
    """Страница урока со всеми шагами в нужном порядке."""

    session_key = _session_key(request)
    lesson = get_object_or_404(
        Lesson.objects.select_related('world'),
        world__slug=world_slug,
        slug=lesson_slug,
    )
    progress = _progress_for_world(session_key, lesson.world)
    if progress.points < lesson.min_points_required:
        return redirect('main:world_detail', slug=lesson.world.slug)
    steps = Quest.objects.filter(lesson=lesson, is_active=True).annotate(
        solved_at=Max(
            'submissions__created_at',
            filter=Q(submissions__session_key=session_key, submissions__is_success=True),
        ),
        failed_at=Max(
            'submissions__created_at',
            filter=Q(submissions__session_key=session_key, submissions__is_success=False),
        ),
        tries=Count('submissions', filter=Q(submissions__session_key=session_key)),
    )
    first_step = steps.first()

    return render(
        request,
        'main/lesson.html',
        {
            'lesson': lesson,
            'steps': steps,
            'first_step': first_step,
            'summary': _student_summary(session_key),
        },
    )


def quest_detail(request, world_slug, quest_slug):
    """Страница задачи с онлайн-редактором и автопроверкой."""

    session_key = _session_key(request)
    quest = get_object_or_404(
        Quest.objects.select_related('world', 'lesson'),
        world__slug=world_slug,
        slug=quest_slug,
    )
    if quest.lesson:
        progress = _progress_for_world(session_key, quest.world)
        if progress.points < quest.lesson.min_points_required:
            return redirect('main:world_detail', slug=quest.world.slug)

    lesson_steps = Quest.objects.filter(lesson=quest.lesson, is_active=True).annotate(
        solved_at=Max(
            'submissions__created_at',
            filter=Q(submissions__session_key=session_key, submissions__is_success=True),
        ),
        failed_at=Max(
            'submissions__created_at',
            filter=Q(submissions__session_key=session_key, submissions__is_success=False),
        ),
    ) if quest.lesson else Quest.objects.none()
    step_ids = list(lesson_steps.values_list('id', flat=True))
    current_index = step_ids.index(quest.id) if quest.id in step_ids else 0
    previous_step = lesson_steps[current_index - 1] if current_index > 0 else None
    next_step = lesson_steps[current_index + 1] if current_index + 1 < len(step_ids) else None
    latest = Submission.objects.filter(session_key=session_key, quest=quest).first()

    if request.method == 'POST':
        already_solved = Submission.objects.filter(
            session_key=session_key,
            quest=quest,
            is_success=True,
        ).exists()
        form = CodeSubmissionForm(request.POST) if quest.task_type == Quest.TaskType.PYTHON else None
        if quest.task_type == Quest.TaskType.PYTHON and form.is_valid():
            answer = form.cleaned_data['code']
            result = check_solution(answer, quest.tests)
            is_success = result.is_success
            passed_tests = result.passed_tests
            total_tests = result.total_tests
            feedback = result.feedback
        elif quest.task_type != Quest.TaskType.PYTHON:
            answer, is_success, passed_tests, total_tests, feedback = _check_non_python_answer(quest, request)
        else:
            answer = ''
            is_success = False
            passed_tests = 0
            total_tests = 1
            feedback = 'Проверьте, что код заполнен.'

        Submission.objects.create(
            quest=quest,
            session_key=session_key,
            code=answer,
            is_success=is_success,
            passed_tests=passed_tests,
            total_tests=total_tests,
            feedback=feedback,
        )

        if is_success and not already_solved:
            _save_success_progress(session_key, quest)

        return redirect('main:quest_detail', world_slug=quest.world.slug, quest_slug=quest.slug)
    else:
        initial_code = latest.code if latest else quest.starter_code
        form = CodeSubmissionForm(initial={'code': initial_code}) if quest.task_type == Quest.TaskType.PYTHON else None

    failed_attempts = Submission.objects.filter(
        session_key=session_key,
        quest=quest,
        is_success=False,
    ).count()

    return render(
        request,
        'main/quest.html',
        {
            'quest': quest,
            'form': form,
            'latest': latest,
            'show_hint': failed_attempts >= 1,
            'show_easier': failed_attempts >= 2,
            'summary': _student_summary(session_key),
            'lesson_steps': lesson_steps,
            'current_index': current_index,
            'previous_step': previous_step,
            'next_step': next_step,
        },
    )


def progress_view(request):
    """Страница прогресса со сводкой, графиком и историей решений."""

    session_key = _session_key(request)
    progress_items = Progress.objects.filter(session_key=session_key).select_related('world')
    submissions = Submission.objects.filter(session_key=session_key).select_related('quest', 'quest__world')[:20]

    return render(
        request,
        'main/progress.html',
        {
            'progress_items': progress_items,
            'submissions': submissions,
            'summary': _student_summary(session_key),
        },
    )


def career_view(request):
    """Страница игрового прогресса: карьера химика и улучшения персонажа."""

    session_key = _session_key(request)
    active_upgrades = set(request.session.get('chemist_upgrades', []))

    if request.method == 'POST':
        upgrade_id = request.POST.get('upgrade_id')
        state = _chemist_state(session_key, active_upgrades)
        allowed_ids = {
            upgrade['id']
            for upgrade in state['upgrades']
            if upgrade['is_unlocked']
        }
        if upgrade_id in allowed_ids:
            active_upgrades.add(upgrade_id)
            request.session['chemist_upgrades'] = sorted(active_upgrades)
            request.session.modified = True
        return redirect('main:career')

    state = _chemist_state(session_key, active_upgrades)
    return render(
        request,
        'main/career.html',
        {
            **state,
            'summary': state['summary'],
        },
    )


def textbooks_view(request):
    """Учебники со справочной теорией по курсам платформы."""

    session_key = _session_key(request)
    return render(
        request,
        'main/textbooks.html',
        {
            'textbooks': TEXTBOOKS,
            'summary': _student_summary(session_key),
        },
    )


def textbook_detail(request, book_slug):
    """Оглавление одного учебника."""

    session_key = _session_key(request)
    book = _get_textbook(book_slug)
    return render(
        request,
        'main/textbook_detail.html',
        {
            'book': book,
            'summary': _student_summary(session_key),
        },
    )


def textbook_topic_detail(request, book_slug, topic_slug):
    """Отдельная страница темы учебника."""

    session_key = _session_key(request)
    book = _get_textbook(book_slug)
    topic = _get_textbook_topic(book, topic_slug)
    topics = book['topics']
    current_index = topics.index(topic)
    previous_topic = topics[current_index - 1] if current_index > 0 else None
    next_topic = topics[current_index + 1] if current_index + 1 < len(topics) else None
    return render(
        request,
        'main/textbook_topic.html',
        {
            'book': book,
            'topic': topic,
            'previous_topic': previous_topic,
            'next_topic': next_topic,
            'summary': _student_summary(session_key),
        },
    )


def reset_progress(request):
    """Сбрасывает прогресс только после явного подтверждения.

    Клиент показывает окно подтверждения, а сервер дополнительно требует
    скрытое поле confirm_reset. Так случайный GET-запрос ничего не удалит.
    """

    session_key = _session_key(request)
    if request.method == 'POST' and request.POST.get('confirm_reset') == 'RESET':
        Submission.objects.filter(session_key=session_key).delete()
        Progress.objects.filter(session_key=session_key).delete()
        request.session.pop('chemist_upgrades', None)
    return redirect('main:progress')
