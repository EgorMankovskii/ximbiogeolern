from django.db import migrations


WORLDS = [
    {
        'slug': 'biology',
        'title': 'Биология',
        'subject': 'Живые системы',
        'intro': 'Исследуйте клетки, экосистемы и популяции через Python-задачи.',
        'color': '#1f8a5b',
        'accent': '#7bd389',
        'icon': 'leaf',
        'order': 1,
        'quests': [
            {
                'slug': 'chlorophyll-average',
                'title': 'Индекс хлорофилла',
                'difficulty': 1,
                'story': 'Ботаническая станция получила измерения хлорофилла по листьям. Нужно быстро посчитать средний индекс.',
                'theory': 'Хлорофилл помогает растениям поглощать свет. Среднее значение показывает общее состояние выборки.',
                'starter_code': 'def solve(values):\n    # Верните среднее значение списка values.\n    pass\n',
                'tests': [
                    {'args': [[10, 12, 14]], 'expected': 12},
                    {'args': [[7, 9]], 'expected': 8},
                    {'args': [[5]], 'expected': 5},
                ],
                'hint': 'Сложите значения через sum(values) и разделите на len(values).',
                'easier_text': 'Для начала решите частный случай: список всегда содержит хотя бы одно число.',
                'reward_points': 20,
                'visual_kind': 'leaf-chart',
                'order': 1,
            },
            {
                'slug': 'population-growth',
                'title': 'Рост популяции',
                'difficulty': 2,
                'story': 'Экологи сравнивают численность вида по годам. Нужно найти годы, где популяция выросла.',
                'theory': 'Рост популяции считают по переходам между соседними наблюдениями.',
                'starter_code': 'def solve(values):\n    # Верните количество переходов, где следующее число больше предыдущего.\n    pass\n',
                'tests': [
                    {'args': [[10, 12, 11, 18]], 'expected': 2},
                    {'args': [[5, 5, 4]], 'expected': 0},
                    {'args': [[1, 2, 3, 4]], 'expected': 3},
                ],
                'hint': 'Сравните пары values[i] и values[i + 1] в цикле.',
                'easier_text': 'Сначала попробуйте вывести все соседние пары, а потом добавьте счетчик.',
                'reward_points': 35,
                'visual_kind': 'population',
                'order': 2,
            },
        ],
    },
    {
        'slug': 'chemistry',
        'title': 'Химия',
        'subject': 'Лаборатория веществ',
        'intro': 'Собирайте молекулы, анализируйте реакции и тренируйте алгоритмическое мышление.',
        'color': '#7c4dff',
        'accent': '#00bcd4',
        'icon': 'flask',
        'order': 2,
        'quests': [
            {
                'slug': 'molecule-mass',
                'title': 'Масса молекулы',
                'difficulty': 1,
                'story': 'Лабораторный терминал передал массы атомов в молекуле. Найдите суммарную массу.',
                'theory': 'Молекулярная масса равна сумме атомных масс элементов в составе молекулы.',
                'starter_code': 'def solve(atom_masses):\n    # Верните сумму масс атомов.\n    pass\n',
                'tests': [
                    {'args': [[1, 1, 16]], 'expected': 18},
                    {'args': [[12, 16, 16]], 'expected': 44},
                    {'args': [[23, 35]], 'expected': 58},
                ],
                'hint': 'Для суммы списка в Python есть функция sum.',
                'easier_text': 'Представьте, что atom_masses = [1, 1, 16]. Как получить 18?',
                'reward_points': 20,
                'visual_kind': 'molecule',
                'order': 1,
            },
            {
                'slug': 'reaction-balance',
                'title': 'Баланс реагентов',
                'difficulty': 3,
                'story': 'Перед запуском реакции нужно проверить, хватает ли каждого реагента.',
                'theory': 'Реакция возможна, если по каждому веществу запас не меньше требуемого количества.',
                'starter_code': 'def solve(required, available):\n    # Верните True, если всех реагентов достаточно, иначе False.\n    pass\n',
                'tests': [
                    {'args': [{'H': 2, 'O': 1}, {'H': 3, 'O': 1}], 'expected': True},
                    {'args': [{'C': 1, 'O': 2}, {'C': 1, 'O': 1}], 'expected': False},
                    {'args': [{}, {'Na': 1}], 'expected': True},
                ],
                'hint': 'Пройдите по required.items() и сравните с available.get(name, 0).',
                'easier_text': 'Начните с одного реагента: если available меньше required, сразу возвращайте False.',
                'reward_points': 50,
                'visual_kind': 'reaction',
                'order': 2,
            },
        ],
    },
    {
        'slug': 'geography',
        'title': 'География',
        'subject': 'Карты и маршруты',
        'intro': 'Работайте с координатами, высотами, расстояниями и климатическими наблюдениями.',
        'color': '#2f80ed',
        'accent': '#f2c94c',
        'icon': 'map',
        'order': 3,
        'quests': [
            {
                'slug': 'highest-point',
                'title': 'Самая высокая точка',
                'difficulty': 1,
                'story': 'Картографическая группа собрала высоты точек маршрута. Найдите максимум.',
                'theory': 'Максимальная высота помогает выбрать обзорные точки и оценить сложность маршрута.',
                'starter_code': 'def solve(heights):\n    # Верните максимальную высоту.\n    pass\n',
                'tests': [
                    {'args': [[120, 340, 210]], 'expected': 340},
                    {'args': [[-5, 0, 12]], 'expected': 12},
                    {'args': [[77]], 'expected': 77},
                ],
                'hint': 'Функция max возвращает наибольший элемент списка.',
                'easier_text': 'Список heights всегда непустой, поэтому можно сразу искать максимум.',
                'reward_points': 20,
                'visual_kind': 'terrain',
                'order': 1,
            },
            {
                'slug': 'route-distance',
                'title': 'Длина маршрута',
                'difficulty': 2,
                'story': 'Навигатор получил последовательность отметок на прямой. Нужно посчитать общий путь.',
                'theory': 'Полная длина маршрута складывается из расстояний между соседними точками.',
                'starter_code': 'def solve(points):\n    # Верните сумму расстояний между соседними точками.\n    pass\n',
                'tests': [
                    {'args': [[0, 3, 7]], 'expected': 7},
                    {'args': [[10, 4, 4, 1]], 'expected': 9},
                    {'args': [[5]], 'expected': 0},
                ],
                'hint': 'Расстояние на прямой считается как abs(points[i + 1] - points[i]).',
                'easier_text': 'Если точка одна, идти некуда, значит расстояние равно 0.',
                'reward_points': 35,
                'visual_kind': 'route',
                'order': 2,
            },
        ],
    },
]


def seed_worlds(apps, schema_editor):
    World = apps.get_model('main', 'World')
    Quest = apps.get_model('main', 'Quest')

    for world_data in WORLDS:
        quests = world_data.pop('quests')
        world, _ = World.objects.update_or_create(slug=world_data['slug'], defaults=world_data)
        for quest_data in quests:
            Quest.objects.update_or_create(
                slug=quest_data['slug'],
                defaults={**quest_data, 'world': world, 'is_active': True},
            )
        world_data['quests'] = quests


def remove_worlds(apps, schema_editor):
    World = apps.get_model('main', 'World')
    World.objects.filter(slug__in=[item['slug'] for item in WORLDS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_worlds, remove_worlds),
    ]
