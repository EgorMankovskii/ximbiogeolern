from django.db import models
from django.utils import timezone


class Course(models.Model):
    """Курс объединяет модули и задачи одной учебной программы.

    Например, сейчас есть курс Python. Позже можно добавить JavaScript, SQL
    или Django: для этого не нужно менять код, достаточно создать курс в админке.
    """

    title = models.CharField('Название курса', max_length=120)
    slug = models.SlugField('Адрес курса', unique=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title


class CourseModule(models.Model):
    """Модуль внутри курса.

    Модуль нужен, чтобы курс можно было расширять постепенно: сначала один блок
    задач по Python, потом отдельные блоки по строкам, ООП, Django и так далее.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField('Название модуля', max_length=120)
    slug = models.SlugField('Адрес модуля')
    description = models.TextField('Описание', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=1)

    class Meta:
        ordering = ['course__title', 'order', 'title']
        unique_together = ['course', 'slug']
        verbose_name = 'модуль курса'
        verbose_name_plural = 'модули курсов'

    def __str__(self):
        return f'{self.course}: {self.title}'


class Exercise(models.Model):
    """Учебная задача внутри модуля курса.

    Модель хранит не только текст задания, но и тесты. Это удобно для учебного
    проекта: контентом можно управлять из админки, не меняя код приложения.
    """

    class Difficulty(models.IntegerChoices):
        EASY = 1, 'Легко'
        MEDIUM = 2, 'Средне'
        HARD = 3, 'Сложно'

    module = models.ForeignKey(
        CourseModule,
        on_delete=models.PROTECT,
        related_name='exercises',
        verbose_name='Модуль',
        null=True,
    )
    title = models.CharField('Название', max_length=120)
    slug = models.SlugField('Адрес', unique=True)
    topic = models.CharField('Тема', max_length=80)
    difficulty = models.PositiveSmallIntegerField('Сложность', choices=Difficulty.choices)
    short_description = models.CharField('Короткое описание', max_length=220)
    task_text = models.TextField('Условие')
    starter_code = models.TextField('Стартовый код')
    tests = models.JSONField('Тесты')
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        ordering = ['module__order', 'difficulty', 'topic', 'title']
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'

    def __str__(self):
        return self.title


class Attempt(models.Model):
    """Одна отправка решения учеником.

    Пользователя здесь заменяет session_key. Так сайт можно попробовать без
    регистрации, но прогресс все равно сохраняется в рамках браузерной сессии.
    """

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='attempts')
    session_key = models.CharField('Сессия ученика', max_length=40, db_index=True)
    code = models.TextField('Код решения')
    is_success = models.BooleanField('Решено', default=False)
    passed_tests = models.PositiveSmallIntegerField('Пройдено тестов', default=0)
    total_tests = models.PositiveSmallIntegerField('Всего тестов', default=0)
    feedback = models.TextField('Обратная связь')
    created_at = models.DateTimeField('Когда отправлено', default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'

    def __str__(self):
        status = 'успех' if self.is_success else 'ошибка'
        return f'{self.exercise}: {status}'
