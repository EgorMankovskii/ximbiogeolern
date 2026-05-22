from django.db import models
from django.utils import timezone


class World(models.Model):
    """Научный раздел платформы: биология, химия или география.

    Если нужно добавить новый предмет, junior-разработчику не придется менять
    шаблоны: достаточно создать новый World и привязать к нему задачи.
    """

    title = models.CharField('Название мира', max_length=80)
    slug = models.SlugField('URL-адрес', unique=True)
    subject = models.CharField('Предмет', max_length=80)
    intro = models.TextField('Короткое описание')
    color = models.CharField('Основной цвет', max_length=20, default='#2f80ed')
    accent = models.CharField('Акцентный цвет', max_length=20, default='#27ae60')
    icon = models.CharField('Иконка', max_length=40, default='spark')
    order = models.PositiveSmallIntegerField('Порядок', default=1)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'научный мир'
        verbose_name_plural = 'научные миры'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Урок внутри научного мира.

    Один урок состоит из нескольких шагов Quest: сначала может быть теория или
    тест, затем сопоставление, затем Python-задача. Так структура становится
    похожей на Stepik, где ученик проходит материал постепенно.
    """

    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField('Название урока', max_length=120)
    slug = models.SlugField('URL-адрес урока')
    theme = models.CharField('Тема внутри мира', max_length=120, default='Основные темы')
    intro = models.TextField('Описание урока')
    min_points_required = models.PositiveIntegerField('RP для открытия', default=0)
    order = models.PositiveSmallIntegerField('Порядок', default=1)
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        ordering = ['world__order', 'order', 'title']
        unique_together = ['world', 'slug']
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.world}: {self.title}'


class Quest(models.Model):
    """Задание внутри научного мира.

    Задание может быть Python-задачей, тестом или сопоставлением. Общие поля
    отвечают за сюжет и справку, а JSON-поле content хранит данные конкретного
    типа задания: варианты ответа, пары для сопоставления или визуальные подписи.
    """

    class Difficulty(models.IntegerChoices):
        NOVICE = 1, 'Новичок'
        RESEARCHER = 2, 'Исследователь'
        EXPERT = 3, 'Эксперт'

    class TaskType(models.TextChoices):
        PYTHON = 'python', 'Python'
        QUIZ = 'quiz', 'Тест'
        MATCH = 'match', 'Сопоставление'

    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='quests')
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='steps',
        null=True,
        blank=True,
        verbose_name='Урок',
    )
    title = models.CharField('Название задачи', max_length=120)
    slug = models.SlugField('URL-адрес', unique=True)
    task_type = models.CharField('Тип задания', max_length=20, choices=TaskType.choices, default=TaskType.PYTHON)
    difficulty = models.PositiveSmallIntegerField('Сложность', choices=Difficulty.choices)
    story = models.TextField('Сюжет задачи')
    theory = models.TextField('Предметная справка')
    starter_code = models.TextField('Стартовый код', blank=True)
    tests = models.JSONField('Тесты Python', default=list, blank=True)
    content = models.JSONField('Данные задания', default=dict, blank=True)
    hint = models.TextField('Подсказка')
    easier_text = models.TextField('Упрощенный вариант', blank=True)
    reward_points = models.PositiveSmallIntegerField('Баллы', default=20)
    visual_kind = models.CharField('Тип визуализации', max_length=40, default='chart')
    order = models.PositiveSmallIntegerField('Порядок', default=1)
    step_order = models.PositiveSmallIntegerField('Порядок шага в уроке', default=1)
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        ordering = ['world__order', 'lesson__order', 'step_order', 'difficulty', 'order', 'title']
        verbose_name = 'квест'
        verbose_name_plural = 'квесты'

    def __str__(self):
        return self.title


class Progress(models.Model):
    """Прогресс ученика в рамках браузерной сессии.

    Пока нет авторизации, сессия заменяет пользователя. Позже это поле можно
    заменить или дополнить ForeignKey на User.
    """

    session_key = models.CharField('Сессия', max_length=40, db_index=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='progress_items')
    points = models.PositiveIntegerField('Баллы', default=0)
    solved_count = models.PositiveSmallIntegerField('Решено задач', default=0)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        unique_together = ['session_key', 'world']
        verbose_name = 'прогресс'
        verbose_name_plural = 'прогресс'

    def __str__(self):
        return f'{self.world}: {self.points} баллов'


class Submission(models.Model):
    """Одна отправка решения.

    Сохраняем код и обратную связь, чтобы на странице прогресса показать историю
    и понять, какие задачи даются ученику сложно.
    """

    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='submissions')
    session_key = models.CharField('Сессия', max_length=40, db_index=True)
    code = models.TextField('Код ученика')
    is_success = models.BooleanField('Решено', default=False)
    passed_tests = models.PositiveSmallIntegerField('Пройдено тестов', default=0)
    total_tests = models.PositiveSmallIntegerField('Всего тестов', default=0)
    feedback = models.TextField('Комментарий проверки')
    created_at = models.DateTimeField('Дата отправки', default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'отправка'
        verbose_name_plural = 'отправки'

    def __str__(self):
        status = 'успех' if self.is_success else 'ошибка'
        return f'{self.quest}: {status}'
