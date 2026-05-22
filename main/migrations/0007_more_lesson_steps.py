from django.db import migrations


EXTRA_STEPS = {
    'biology': [
        {
            'lesson_slug': 'ecosystem-and-cells',
            'slug': 'enzyme-temperature-quiz',
            'title': 'Ферменты и температура',
            'task_type': 'quiz',
            'difficulty': 2,
            'step_order': 5,
            'order': 5,
            'story': 'Фермент работал при 37 градусах, а затем пробирку сильно нагрели. Как изменится скорость реакции?',
            'theory': 'Ферменты имеют оптимальные условия работы. Слишком высокая температура может нарушить структуру белка.',
            'content': {
                'correct': 'denaturation',
                'options': [
                    {'value': 'faster_forever', 'label': 'Скорость будет бесконечно расти при нагреве'},
                    {'value': 'denaturation', 'label': 'После перегрева фермент может потерять активность'},
                    {'value': 'no_change', 'label': 'Температура не влияет на ферменты'},
                    {'value': 'becomes_sugar', 'label': 'Фермент превращается в глюкозу'},
                ],
            },
            'starter_code': '',
            'tests': [],
            'hint': 'Ферменты - белки, а белки чувствительны к сильному нагреву.',
            'easier_text': 'Вспомните, что происходит с белком яйца при нагревании.',
            'reward_points': 25,
            'visual_kind': 'enzyme',
        },
        {
            'lesson_slug': 'ecosystem-and-cells',
            'slug': 'dna-pair-count',
            'title': 'Подсчет пар ДНК',
            'task_type': 'python',
            'difficulty': 2,
            'step_order': 6,
            'order': 6,
            'story': 'Дана строка ДНК. Посчитайте, сколько раз в ней встречается каждая буква A, T, G и C.',
            'theory': 'В ДНК четыре основных нуклеотида: A, T, G и C. Подсчет частот помогает анализировать участок последовательности.',
            'starter_code': 'def solve(dna):\n    # Верните словарь с ключами A, T, G, C и количеством букв.\n    pass\n',
            'tests': [
                {'args': ['AATGC'], 'expected': {'A': 2, 'T': 1, 'G': 1, 'C': 1}},
                {'args': ['GGCC'], 'expected': {'A': 0, 'T': 0, 'G': 2, 'C': 2}},
                {'args': [''], 'expected': {'A': 0, 'T': 0, 'G': 0, 'C': 0}},
            ],
            'content': {},
            'hint': 'Создайте словарь с нулями, затем пройдите по строке циклом.',
            'easier_text': 'Начните с result = {"A": 0, "T": 0, "G": 0, "C": 0}.',
            'reward_points': 40,
            'visual_kind': 'dna',
        },
    ],
    'chemistry': [
        {
            'lesson_slug': 'lab-and-formulas',
            'slug': 'acid-base-indicator',
            'title': 'Индикатор и среда раствора',
            'task_type': 'quiz',
            'difficulty': 2,
            'step_order': 5,
            'order': 5,
            'story': 'Лакмус стал красным в растворе. Какой вывод наиболее вероятен?',
            'theory': 'Индикаторы меняют цвет в зависимости от кислотности среды. Лакмус краснеет в кислой среде.',
            'content': {
                'correct': 'acid',
                'options': [
                    {'value': 'acid', 'label': 'Раствор имеет кислую среду'},
                    {'value': 'alkali', 'label': 'Раствор точно щелочной'},
                    {'value': 'neutral_only', 'label': 'Раствор обязательно нейтральный'},
                    {'value': 'metal', 'label': 'В растворе обязательно есть металл'},
                ],
            },
            'starter_code': '',
            'tests': [],
            'hint': 'Красный лакмус связан с кислой средой.',
            'easier_text': 'Сравните слова: кислота часто ассоциируется с красным лакмусом.',
            'reward_points': 25,
            'visual_kind': 'indicator',
        },
        {
            'lesson_slug': 'lab-and-formulas',
            'slug': 'solution-concentration',
            'title': 'Концентрация раствора',
            'task_type': 'python',
            'difficulty': 2,
            'step_order': 6,
            'order': 6,
            'story': 'Нужно вычислить массовую долю вещества в процентах по массе вещества и массе раствора.',
            'theory': 'Массовая доля = масса вещества / масса раствора * 100%.',
            'starter_code': 'def solve(solute_mass, solution_mass):\n    # Верните массовую долю в процентах.\n    pass\n',
            'tests': [
                {'args': [10, 100], 'expected': 10},
                {'args': [5, 20], 'expected': 25},
                {'args': [2, 50], 'expected': 4},
            ],
            'content': {},
            'hint': 'Сначала разделите solute_mass на solution_mass, затем умножьте на 100.',
            'easier_text': 'Для 10 г вещества в 100 г раствора ответ 10%.',
            'reward_points': 40,
            'visual_kind': 'concentration',
        },
    ],
    'geography': [
        {
            'lesson_slug': 'maps-climate-routes',
            'slug': 'scale-distance-quiz',
            'title': 'Масштаб карты',
            'task_type': 'quiz',
            'difficulty': 2,
            'step_order': 5,
            'order': 5,
            'story': 'На карте масштаба 1:100 000 расстояние между поселками 3 см. Какое расстояние на местности?',
            'theory': 'Масштаб 1:100 000 означает, что 1 см на карте равен 100 000 см, то есть 1 км на местности.',
            'content': {
                'correct': '3km',
                'options': [
                    {'value': '300m', 'label': '300 метров'},
                    {'value': '3km', 'label': '3 километра'},
                    {'value': '30km', 'label': '30 километров'},
                    {'value': '100km', 'label': '100 километров'},
                ],
            },
            'starter_code': '',
            'tests': [],
            'hint': 'При масштабе 1:100 000 один сантиметр на карте равен одному километру.',
            'easier_text': 'Если 1 см = 1 км, то 3 см = 3 км.',
            'reward_points': 25,
            'visual_kind': 'scale',
        },
        {
            'lesson_slug': 'maps-climate-routes',
            'slug': 'temperature-amplitude',
            'title': 'Амплитуда температур',
            'task_type': 'python',
            'difficulty': 2,
            'step_order': 6,
            'order': 6,
            'story': 'Даны температуры за неделю. Найдите амплитуду: разницу между максимальной и минимальной температурой.',
            'theory': 'Температурная амплитуда показывает, насколько сильно менялась температура за период.',
            'starter_code': 'def solve(temps):\n    # Верните max(temps) - min(temps).\n    pass\n',
            'tests': [
                {'args': [[-2, 0, 5, 3]], 'expected': 7},
                {'args': [[10, 10, 10]], 'expected': 0},
                {'args': [[-8, -3, 2]], 'expected': 10},
            ],
            'content': {},
            'hint': 'Найдите максимум и минимум списка.',
            'easier_text': 'Для [-2, 0, 5, 3] максимум 5, минимум -2, разница 7.',
            'reward_points': 40,
            'visual_kind': 'temperature',
        },
    ],
}


def add_more_steps(apps, schema_editor):
    Lesson = apps.get_model('main', 'Lesson')
    Quest = apps.get_model('main', 'Quest')

    for steps in EXTRA_STEPS.values():
        for step in steps:
            lesson = Lesson.objects.select_related('world').get(slug=step['lesson_slug'])
            data = {key: value for key, value in step.items() if key != 'lesson_slug'}
            Quest.objects.update_or_create(
                slug=step['slug'],
                defaults={
                    **data,
                    'world': lesson.world,
                    'lesson': lesson,
                    'is_active': True,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_lessons_and_harder_tests'),
    ]

    operations = [
        migrations.RunPython(add_more_steps, migrations.RunPython.noop),
    ]
