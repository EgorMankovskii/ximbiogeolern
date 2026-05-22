from django.db import migrations, models


LESSON_THEMES = {
    'dna-sequence-research': 'Биоинформатика',
    'protein-sequence-research': 'Биоинформатика',
    'species-dna-comparison': 'Биоинформатика',
    'population-simulation': 'Популяции и эволюция',
    'evolution-simulation': 'Популяции и эволюция',
    'mendel-genetics': 'Генетика',
    'phenotype-prediction': 'Генетика',
    'ecosystem-data-analysis': 'Экосистемы и микробиом',
    'microbiome-analysis': 'Экосистемы и микробиом',
    'cell-image-processing': 'Клеточные данные',
    'lab-and-formulas': 'Лабораторные расчеты',
    'reactor-concentration': 'Лабораторные расчеты',
    'maps-climate-routes': 'Карты и климат',
    'expedition-data': 'Экспедиционные данные',
}


def fill_lesson_themes(apps, schema_editor):
    Lesson = apps.get_model('main', 'Lesson')
    for slug, theme in LESSON_THEMES.items():
        Lesson.objects.filter(slug=slug).update(theme=theme)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_fix_species_gc_similarity'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='theme',
            field=models.CharField(default='Основные темы', max_length=120, verbose_name='Тема внутри мира'),
        ),
        migrations.RunPython(fill_lesson_themes, migrations.RunPython.noop),
    ]
