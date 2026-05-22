from django.contrib import admin
from django.utils.html import format_html

from .models import Lesson, Progress, Quest, Submission, World


admin.site.site_header = 'EduQuest Admin'
admin.site.site_title = 'EduQuest Admin'
admin.site.index_title = 'Панель управления контентом'


class QuestInline(admin.TabularInline):
    """Показывает шаги урока прямо в карточке урока или мира."""

    model = Quest
    extra = 0
    fields = ('title', 'task_type', 'difficulty', 'step_order', 'reward_points', 'is_active')
    show_change_link = True


class LessonInline(admin.TabularInline):
    """Показывает уроки прямо на странице научного мира."""

    model = Lesson
    extra = 0
    fields = ('title', 'slug', 'theme', 'order', 'is_active')
    show_change_link = True


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    """Админка для предметных разделов EduQuest."""

    list_display = ('title', 'subject', 'color_preview', 'lessons_total', 'quests_total', 'order')
    list_display_links = ('title',)
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'subject', 'intro')
    ordering = ('order', 'title')
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'subject', 'intro')}),
        ('Визуальный стиль', {'fields': ('color', 'accent', 'icon')}),
        ('Публикация', {'fields': ('order',)}),
    )
    inlines = [LessonInline]

    @admin.display(description='Цвет')
    def color_preview(self, obj):
        return format_html(
            '<span class="admin-color-dot" style="--admin-dot:{}"></span><code>{}</code>',
            obj.color,
            obj.color,
        )

    @admin.display(description='Уроки')
    def lessons_total(self, obj):
        return obj.lessons.count()

    @admin.display(description='Квесты')
    def quests_total(self, obj):
        return obj.quests.count()


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Уроки объединяют несколько шагов: тесты, сопоставления и Python."""

    list_display = ('title', 'world', 'theme', 'steps_total', 'min_points_required', 'order', 'status_badge')
    list_display_links = ('title',)
    list_editable = ('min_points_required', 'order')
    list_filter = ('world', 'theme', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'intro')
    ordering = ('world__order', 'order', 'title')
    fieldsets = (
        ('Привязка', {'fields': ('world', 'theme')}),
        ('Материал', {'fields': ('title', 'slug', 'intro')}),
        ('Доступность', {'fields': ('min_points_required', 'order', 'is_active')}),
    )
    inlines = [QuestInline]

    @admin.display(description='Шаги')
    def steps_total(self, obj):
        return obj.steps.count()

    @admin.display(description='Статус', ordering='is_active')
    def status_badge(self, obj):
        label = 'Опубликован' if obj.is_active else 'Скрыт'
        tone = 'good' if obj.is_active else 'muted'
        return format_html('<span class="admin-pill {}">{}</span>', tone, label)


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    """Админка для задач: здесь удобно добавлять тесты и подсказки."""

    list_display = (
        'title',
        'world',
        'lesson',
        'task_type_badge',
        'difficulty_badge',
        'step_order',
        'reward_points',
        'status_badge',
    )
    list_display_links = ('title',)
    list_editable = ('step_order', 'reward_points')
    list_filter = ('world', 'lesson', 'task_type', 'difficulty', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'story', 'theory')
    ordering = ('world__order', 'lesson__order', 'step_order', 'title')
    fieldsets = (
        ('Привязка и порядок', {'fields': ('world', 'lesson', 'order', 'step_order', 'is_active')}),
        ('Задание', {'fields': ('title', 'slug', 'task_type', 'difficulty', 'reward_points')}),
        ('Сюжет и теория', {'fields': ('story', 'theory', 'hint', 'easier_text')}),
        ('Проверка и данные', {'fields': ('starter_code', 'tests', 'content')}),
        ('Визуальный результат', {'fields': ('visual_kind',)}),
    )
    list_per_page = 30

    @admin.display(description='Тип', ordering='task_type')
    def task_type_badge(self, obj):
        return format_html('<span class="admin-pill info">{}</span>', obj.get_task_type_display())

    @admin.display(description='Сложность', ordering='difficulty')
    def difficulty_badge(self, obj):
        tones = {1: 'good', 2: 'warn', 3: 'danger'}
        return format_html('<span class="admin-pill {}">{}</span>', tones.get(obj.difficulty, 'muted'), obj.get_difficulty_display())

    @admin.display(description='Статус', ordering='is_active')
    def status_badge(self, obj):
        label = 'На сайте' if obj.is_active else 'Скрыт'
        tone = 'good' if obj.is_active else 'muted'
        return format_html('<span class="admin-pill {}">{}</span>', tone, label)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    """Прогресс нужен для отладки и анализа прохождения."""

    list_display = ('session_key', 'world', 'points', 'solved_count', 'updated_at')
    list_filter = ('world',)
    search_fields = ('session_key',)
    readonly_fields = ('session_key', 'world', 'points', 'solved_count', 'updated_at')
    date_hierarchy = 'updated_at'
    list_per_page = 40


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """История отправок помогает искать неудачные формулировки задач."""

    list_display = ('quest', 'session_key', 'result_badge', 'tests_score', 'created_at')
    list_filter = ('is_success', 'quest__world', 'quest__difficulty')
    search_fields = ('session_key', 'quest__title', 'feedback')
    readonly_fields = ('quest', 'session_key', 'code', 'is_success', 'passed_tests', 'total_tests', 'feedback', 'created_at')
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
