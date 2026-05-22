from django.db import migrations


def create_python_course(apps, schema_editor):
    Course = apps.get_model('lessons', 'Course')
    CourseModule = apps.get_model('lessons', 'CourseModule')
    Exercise = apps.get_model('lessons', 'Exercise')

    course, _ = Course.objects.update_or_create(
        slug='python',
        defaults={
            'title': 'Python',
            'description': 'Базовый курс по Python: функции, списки, строки, словари и первые алгоритмы.',
            'is_active': True,
        },
    )
    module, _ = CourseModule.objects.update_or_create(
        course=course,
        slug='python-basics',
        defaults={
            'title': 'Основы Python',
            'description': 'Все текущие задачи собраны в одном модуле, чтобы курс был цельным и понятным.',
            'order': 1,
        },
    )
    Exercise.objects.filter(module__isnull=True).update(module=module)


def remove_python_course(apps, schema_editor):
    Course = apps.get_model('lessons', 'Course')
    Exercise = apps.get_model('lessons', 'Exercise')
    Exercise.objects.filter(module__course__slug='python').update(module=None)
    Course.objects.filter(slug='python').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_course_alter_exercise_options_coursemodule_and_more'),
    ]

    operations = [
        migrations.RunPython(create_python_course, remove_python_course),
    ]
