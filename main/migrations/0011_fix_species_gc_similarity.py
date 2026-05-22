from django.db import migrations


def fix_species_gc_similarity(apps, schema_editor):
    Quest = apps.get_model('main', 'Quest')
    Quest.objects.filter(slug='compare-species-dna').update(
        tests=[
            {
                'args': ['ATGC', 'ATGT'],
                'expected': {
                    'identity_percent': 75.0,
                    'mutations': [[4, 'C', 'T']],
                    'gc_similarity': 75.0,
                },
            },
            {
                'args': ['GGCC', 'GGCC'],
                'expected': {
                    'identity_percent': 100.0,
                    'mutations': [],
                    'gc_similarity': 100.0,
                },
            },
        ],
    )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_biology_research_module'),
    ]

    operations = [
        migrations.RunPython(fix_species_gc_similarity, migrations.RunPython.noop),
    ]
