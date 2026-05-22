from secrets import token_urlsafe

from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SolutionForm
from .models import Attempt, Course, CourseModule, Exercise
from .services import check_solution, recommend_difficulty


def _session_key(request):
    """Возвращает стабильный учебный ключ без записи в DB-сессии."""

    key = request.session.get('student_key') or request.session.session_key
    if not key:
        key = token_urlsafe(24)
    request.session['student_key'] = key
    return key


def _progress_for_session(session_key, course=None):
    """Собирает краткую статистику прогресса для главной страницы."""

    exercise_filter = Q(exercise__is_active=True)
    active_exercises = Exercise.objects.filter(is_active=True)
    if course:
        exercise_filter &= Q(exercise__module__course=course)
        active_exercises = active_exercises.filter(module__course=course)

    solved_ids = Attempt.objects.filter(
        exercise_filter,
        session_key=session_key,
        is_success=True,
    ).values_list('exercise_id', flat=True).distinct()

    total = active_exercises.count()
    solved = solved_ids.count()
    attempts = Attempt.objects.filter(exercise_filter, session_key=session_key).count()
    success_rate = round(solved / total * 100) if total else 0

    return {
        'total': total,
        'solved': solved,
        'attempts': attempts,
        'success_rate': success_rate,
        'recommended_difficulty': recommend_difficulty(success_rate),
    }


def exercise_list(request, course_slug=None):
    """Главная страница: задачи, уровни сложности и адаптивная рекомендация."""

    session_key = _session_key(request)
    courses = Course.objects.filter(is_active=True)
    selected_course = get_object_or_404(courses, slug=course_slug) if course_slug else courses.first()
    progress = _progress_for_session(session_key, selected_course)

    exercises = Exercise.objects.filter(is_active=True).annotate(
        solved_at=Max(
            'attempts__created_at',
            filter=Q(attempts__session_key=session_key, attempts__is_success=True),
        ),
        tries=Count('attempts', filter=Q(attempts__session_key=session_key)),
    )
    if selected_course:
        exercises = exercises.filter(module__course=selected_course)

    exercise_by_module = {}
    for exercise in exercises.select_related('module', 'module__course'):
        exercise_by_module.setdefault(exercise.module_id, []).append(exercise)

    module_sections = []
    if selected_course:
        modules = CourseModule.objects.filter(course=selected_course)
        module_sections = [
            {'module': module, 'exercises': exercise_by_module.get(module.id, [])}
            for module in modules
        ]

    return render(
        request,
        'lessons/exercise_list.html',
        {
            'courses': courses,
            'selected_course': selected_course,
            'module_sections': module_sections,
            'progress': progress,
            'difficulty_labels': dict(Exercise.Difficulty.choices),
        },
    )


def exercise_detail(request, slug):
    """Страница одной задачи: условие, редактор кода и результат проверки."""

    session_key = _session_key(request)
    exercise = get_object_or_404(
        Exercise.objects.select_related('module', 'module__course'),
        slug=slug,
        is_active=True,
    )
    latest_attempt = Attempt.objects.filter(
        session_key=session_key,
        exercise=exercise,
    ).first()

    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            result = check_solution(code, exercise.tests)
            Attempt.objects.create(
                exercise=exercise,
                session_key=session_key,
                code=code,
                is_success=result.is_success,
                passed_tests=result.passed_tests,
                total_tests=result.total_tests,
                feedback=result.feedback,
            )
            return redirect('exercise_detail', slug=exercise.slug)
    else:
        form = SolutionForm(initial={'code': latest_attempt.code if latest_attempt else exercise.starter_code})

    return render(
        request,
        'lessons/exercise_detail.html',
        {
            'exercise': exercise,
            'form': form,
            'latest_attempt': latest_attempt,
        },
    )


def progress_view(request):
    """Отдельная страница прогресса ученика."""

    session_key = _session_key(request)
    attempts = Attempt.objects.filter(session_key=session_key).select_related(
        'exercise',
        'exercise__module',
        'exercise__module__course',
    )[:30]
    progress = _progress_for_session(session_key)
    return render(request, 'lessons/progress.html', {'attempts': attempts, 'progress': progress})
