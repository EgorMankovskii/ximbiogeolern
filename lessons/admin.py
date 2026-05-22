from django.contrib import admin
from django.utils.html import format_html

from .models import Attempt, Course, CourseModule, Exercise


class ModuleInline(admin.TabularInline):
    """Показывает модули прямо на странице курса."""

    model = CourseModule
    extra = 0
    fields = ('title', 'slug', 'order')
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Курсы можно добавлять без изменения кода проекта."""

    list_display = ('title', 'slug', 'modules_total', 'exercises_total', 'status_badge')
    list_display_links = ('title',)
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    fieldsets = (
        ('Курс', {'fields': ('title', 'slug', 'description')}),
        ('Публикация', {'fields': ('is_active',)}),
    )
    inlines = [ModuleInline]

    @admin.display(description='Модули')
    def modules_total(self, obj):
        return obj.modules.count()

    @admin.display(description='Задачи')
    def exercises_total(self, obj):
        return Exercise.objects.filter(module__course=obj).count()

    @admin.display(description='Статус', ordering='is_active')
    def status_badge(self, obj):
        label = 'Активен' if obj.is_active else 'Скрыт'
        tone = 'good' if obj.is_active else 'muted'
        return format_html('<span class="admin-pill {}">{}</span>', tone, label)


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    """Модули группируют задачи внутри курса."""

    list_display = ('title', 'course', 'exercises_total', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)
    list_filter = ('course',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    ordering = ('course__title', 'order', 'title')
    fieldsets = (
        ('Привязка', {'fields': ('course',)}),
        ('Модуль', {'fields': ('title', 'slug', 'description', 'order')}),
    )

    @admin.display(description='Задачи')
    def exercises_total(self, obj):
        return obj.exercises.count()


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Настройки списка задач в админке Django."""

    list_display = ('title', 'module', 'topic', 'difficulty_badge', 'status_badge')
    list_display_links = ('title',)
    list_filter = ('module__course', 'module', 'difficulty', 'topic', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'topic', 'task_text')
    ordering = ('module__course__title', 'module__order', 'difficulty', 'title')
    fieldsets = (
        ('Привязка', {'fields': ('module', 'topic')}),
        ('Задача', {'fields': ('title', 'slug', 'difficulty', 'short_description', 'task_text')}),
        ('Проверка', {'fields': ('starter_code', 'tests')}),
        ('Публикация', {'fields': ('is_active',)}),
    )
    list_per_page = 30

    @admin.display(description='Сложность', ordering='difficulty')
    def difficulty_badge(self, obj):
        tones = {1: 'good', 2: 'warn', 3: 'danger'}
        return format_html('<span class="admin-pill {}">{}</span>', tones.get(obj.difficulty, 'muted'), obj.get_difficulty_display())

    @admin.display(description='Статус', ordering='is_active')
    def status_badge(self, obj):
        label = 'На сайте' if obj.is_active else 'Скрыта'
        tone = 'good' if obj.is_active else 'muted'
        return format_html('<span class="admin-pill {}">{}</span>', tone, label)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """Попытки удобно смотреть при отладке проверки решений."""

    list_display = ('exercise', 'session_key', 'result_badge', 'tests_score', 'created_at')
    list_filter = ('is_success', 'exercise__difficulty')
    search_fields = ('session_key', 'exercise__title')
    readonly_fields = ('exercise', 'session_key', 'code', 'is_success', 'passed_tests', 'total_tests', 'feedback', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 40

    @admin.display(description='Результат', ordering='is_success')
    def result_badge(self, obj):
        label = 'Решено' if obj.is_success else 'Ошибка'
        tone = 'good' if obj.is_success else 'danger'
        return format_html('<span class="admin-pill {}">{}</span>', tone, label)

    @admin.display(description='Тесты')
    def tests_score(self, obj):
        return f'{obj.passed_tests}/{obj.total_tests}'
