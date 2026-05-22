from django.db import migrations


WORLD_UPDATES = {
    'biology': {
        'title': 'Био-купол',
        'subject': 'Биология: живые системы',
        'intro': 'Микроскопическая среда и джунгли, где Python помогает анализировать ДНК, клетки и популяции.',
        'color': '#1f8a5b',
        'accent': '#7bd389',
    },
    'chemistry': {
        'title': 'Квантовая лаборатория',
        'subject': 'Химия: вещества и реакции',
        'intro': 'Неоновая лаборатория для расчетов концентраций, молекулярных масс и виртуальных реакторов.',
        'color': '#7c4dff',
        'accent': '#00bcd4',
    },
    'geography': {
        'title': 'Глобальная карта',
        'subject': 'География: данные и маршруты',
        'intro': 'Интерактивная карта экспедиций, где Python работает с климатом, расстояниями и наборами данных.',
        'color': '#2f80ed',
        'accent': '#f2c94c',
    },
}


ADVANCED_LESSONS = {
    'biology': {
        'slug': 'cell-nucleus',
        'title': 'Клеточное ядро',
        'intro': 'Продвинутый урок по анализу ДНК и синтезу РНК: теория, проверка понимания и Python-скрипт.',
        'min_points_required': 90,
        'order': 2,
        'steps': [
            {
                'slug': 'transcription-quiz',
                'title': 'Что происходит при транскрипции',
                'task_type': 'quiz',
                'difficulty': 2,
                'step_order': 1,
                'story': 'Исследователь видит участок ДНК и должен понять, что получится при синтезе РНК.',
                'theory': 'При транскрипции на основе ДНК строится РНК. В РНК вместо тимина T используется урацил U.',
                'content': {
                    'correct': 'rna_from_dna',
                    'options': [
                        {'value': 'protein_from_sugar', 'label': 'Из сахара строится белок'},
                        {'value': 'rna_from_dna', 'label': 'По ДНК строится молекула РНК'},
                        {'value': 'dna_from_lipid', 'label': 'Из липидов строится ДНК'},
                        {'value': 'salt_from_cell', 'label': 'Клетка превращается в соль'},
                    ],
                },
                'starter_code': '',
                'tests': [],
                'hint': 'Ключевое слово: РНК создается по матрице ДНК.',
                'easier_text': 'Вспомните пару ДНК -> РНК.',
                'reward_points': 25,
                'visual_kind': 'dna',
            },
            {
                'slug': 'dna-rna-pairs-match',
                'title': 'Комплементарные пары',
                'task_type': 'match',
                'difficulty': 2,
                'step_order': 2,
                'story': 'Перед запуском синтеза нужно сопоставить буквы ДНК с буквами РНК.',
                'theory': 'Для учебной модели используем правила: A -> U, T -> A, C -> G, G -> C.',
                'content': {
                    'pairs': [
                        {'picture': 'A', 'prompt': 'A в ДНК', 'answer': 'U'},
                        {'picture': 'T', 'prompt': 'T в ДНК', 'answer': 'A'},
                        {'picture': 'C', 'prompt': 'C в ДНК', 'answer': 'G'},
                        {'picture': 'G', 'prompt': 'G в ДНК', 'answer': 'C'},
                    ],
                    'options': [
                        {'value': 'A', 'label': 'A'},
                        {'value': 'U', 'label': 'U'},
                        {'value': 'G', 'label': 'G'},
                        {'value': 'C', 'label': 'C'},
                    ],
                },
                'starter_code': '',
                'tests': [],
                'hint': 'В РНК нет T, вместо него используется U.',
                'easier_text': 'Начните с A -> U.',
                'reward_points': 30,
                'visual_kind': 'dna',
            },
            {
                'slug': 'restore-rna',
                'title': 'Восстановление цепочки РНК',
                'task_type': 'python',
                'difficulty': 3,
                'step_order': 3,
                'story': 'В лаборатории произошел сбой. Нужно восстановить цепочку РНК из поврежденного фрагмента ДНК.',
                'theory': 'Скрипт заменяет символы по правилу A->U, T->A, C->G, G->C. Так код становится инструментом биологического исследования.',
                'starter_code': 'def solve(dna):\n    # Верните строку РНК по правилам A->U, T->A, C->G, G->C.\n    pass\n',
                'tests': [
                    {'args': ['ATCG'], 'expected': 'UAGC'},
                    {'args': ['AATTCCGG'], 'expected': 'UUAAGGCC'},
                    {'args': [''], 'expected': ''},
                ],
                'content': {},
                'hint': 'Создайте словарь замен и собирайте ответ в новую строку.',
                'easier_text': 'Можно пройти по dna циклом и добавлять mapping[letter].',
                'reward_points': 60,
                'visual_kind': 'rna-helix',
            },
        ],
    },
    'chemistry': {
        'slug': 'reactor-concentration',
        'title': 'Реактор концентрации',
        'intro': 'Урок про массовую долю и запуск виртуального реактора с помощью Python-расчетов.',
        'min_points_required': 90,
        'order': 2,
        'steps': [
            {
                'slug': 'mass-fraction-quiz',
                'title': 'Что такое массовая доля',
                'task_type': 'quiz',
                'difficulty': 2,
                'step_order': 1,
                'story': 'Перед запуском реактора нужно понять формулу массовой доли вещества.',
                'theory': 'Массовая доля показывает, какую часть общей массы составляет нужный элемент или вещество.',
                'content': {
                    'correct': 'part_total',
                    'options': [
                        {'value': 'part_total', 'label': 'Масса части делится на общую массу и умножается на 100%'},
                        {'value': 'only_temperature', 'label': 'Это только температура реакции'},
                        {'value': 'volume_only', 'label': 'Это всегда объем газа'},
                        {'value': 'random', 'label': 'Это случайная величина без формулы'},
                    ],
                },
                'starter_code': '',
                'tests': [],
                'hint': 'В формуле есть масса части и общая масса.',
                'easier_text': 'Ищите ответ с делением на общую массу.',
                'reward_points': 25,
                'visual_kind': 'reaction',
            },
            {
                'slug': 'element-mass-fraction',
                'title': 'Массовая доля элемента',
                'task_type': 'python',
                'difficulty': 3,
                'step_order': 2,
                'story': 'Для запуска реактора нужно вычислить долю выбранного элемента в сложном веществе.',
                'theory': 'Python-словарь удобен для химии: ключ — элемент, значение — его вклад в массу вещества.',
                'starter_code': 'def solve(masses, element):\n    # masses - словарь масс элементов. Верните долю element в процентах.\n    pass\n',
                'tests': [
                    {'args': [{'H': 2, 'O': 16}, 'O'], 'expected': 88.89},
                    {'args': [{'C': 12, 'O': 32}, 'C'], 'expected': 27.27},
                    {'args': [{'Na': 23, 'Cl': 35}, 'K'], 'expected': 0},
                ],
                'content': {},
                'hint': 'Сумма масс = sum(masses.values()). Округлите результат через round(value, 2).',
                'easier_text': 'Если элемента нет в словаре, верните 0.',
                'reward_points': 60,
                'visual_kind': 'reactor',
            },
            {
                'slug': 'reactor-result-match',
                'title': 'Сигналы реактора',
                'task_type': 'match',
                'difficulty': 2,
                'step_order': 3,
                'story': 'Реактор показывает сигналы. Сопоставьте их с состояниями опыта.',
                'theory': 'Визуальный интерфейс помогает быстро понять, безопасен ли опыт и достаточно ли вещества.',
                'content': {
                    'pairs': [
                        {'picture': '🟢', 'prompt': 'Зеленый свет', 'answer': 'ready'},
                        {'picture': '🟡', 'prompt': 'Желтый свет', 'answer': 'warning'},
                        {'picture': '🔴', 'prompt': 'Красный свет', 'answer': 'stop'},
                    ],
                    'options': [
                        {'value': 'ready', 'label': 'Можно запускать реакцию'},
                        {'value': 'warning', 'label': 'Нужна проверка расчетов'},
                        {'value': 'stop', 'label': 'Опыт нужно остановить'},
                    ],
                },
                'starter_code': '',
                'tests': [],
                'hint': 'Цвета работают как обычный светофор.',
                'easier_text': 'Красный — остановка.',
                'reward_points': 30,
                'visual_kind': 'reactor',
            },
        ],
    },
    'geography': {
        'slug': 'expedition-data',
        'title': 'Экспедиционные данные',
        'intro': 'Урок про климатические наборы данных, словари и расчет маршрута по координатам.',
        'min_points_required': 90,
        'order': 2,
        'steps': [
            {
                'slug': 'json-data-quiz',
                'title': 'Почему географы используют JSON',
                'task_type': 'quiz',
                'difficulty': 2,
                'step_order': 1,
                'story': 'Экспедиция передает данные о городах, температуре и осадках в структурированном виде.',
                'theory': 'JSON и словари позволяют хранить пары ключ-значение: город, координаты, температура, осадки.',
                'content': {
                    'correct': 'structured',
                    'options': [
                        {'value': 'structured', 'label': 'Данные удобно хранить по ключам и передавать между системами'},
                        {'value': 'picture_only', 'label': 'JSON нужен только для картинок'},
                        {'value': 'no_data', 'label': 'JSON не подходит для данных'},
                        {'value': 'sound', 'label': 'JSON хранит только звук'},
                    ],
                },
                'starter_code': '',
                'tests': [],
                'hint': 'Вспомните словари Python: ключ -> значение.',
                'easier_text': 'Ищите ответ про структуру данных.',
                'reward_points': 25,
                'visual_kind': 'map',
            },
            {
                'slug': 'climate-average',
                'title': 'Средняя температура станций',
                'task_type': 'python',
                'difficulty': 2,
                'step_order': 2,
                'story': 'Даны данные метеостанций в виде списка словарей. Найдите среднюю температуру.',
                'theory': 'Географические наблюдения часто приходят как наборы структурированных записей.',
                'starter_code': 'def solve(stations):\n    # stations: [{"city": "...", "temp": число}]. Верните среднюю temp.\n    pass\n',
                'tests': [
                    {'args': [[{'city': 'A', 'temp': 10}, {'city': 'B', 'temp': 14}]], 'expected': 12},
                    {'args': [[{'city': 'A', 'temp': -5}, {'city': 'B', 'temp': 5}, {'city': 'C', 'temp': 0}]], 'expected': 0},
                    {'args': [[]], 'expected': 0},
                ],
                'content': {},
                'hint': 'Если список пустой, верните 0. Иначе сложите station["temp"].',
                'easier_text': 'Температуру одной станции можно получить как station["temp"].',
                'reward_points': 45,
                'visual_kind': 'climate',
            },
            {
                'slug': 'coordinate-route',
                'title': 'Маршрут экспедиции',
                'task_type': 'python',
                'difficulty': 3,
                'step_order': 3,
                'story': 'Экспедиция движется по координатной сетке. Нужно посчитать длину маршрута по манхэттенскому расстоянию.',
                'theory': 'Для учебной карты расстояние между точками считаем как |x2-x1| + |y2-y1|.',
                'starter_code': 'def solve(points):\n    # points = [[x, y], ...]. Верните сумму расстояний между соседними точками.\n    pass\n',
                'tests': [
                    {'args': [[[0, 0], [2, 1], [2, 4]]], 'expected': 6},
                    {'args': [[[1, 1], [1, 1]]], 'expected': 0},
                    {'args': [[]], 'expected': 0},
                ],
                'content': {},
                'hint': 'Для каждой пары соседних точек сложите abs(dx) + abs(dy).',
                'easier_text': 'Если точек меньше двух, расстояние равно 0.',
                'reward_points': 60,
                'visual_kind': 'route',
            },
        ],
    },
}


def align_report_content(apps, schema_editor):
    World = apps.get_model('main', 'World')
    Lesson = apps.get_model('main', 'Lesson')
    Quest = apps.get_model('main', 'Quest')

    for slug, data in WORLD_UPDATES.items():
        World.objects.filter(slug=slug).update(**data)

    for world_slug, lesson_data in ADVANCED_LESSONS.items():
        world = World.objects.get(slug=world_slug)
        lesson, _ = Lesson.objects.update_or_create(
            world=world,
            slug=lesson_data['slug'],
            defaults={
                'title': lesson_data['title'],
                'intro': lesson_data['intro'],
                'min_points_required': lesson_data['min_points_required'],
                'order': lesson_data['order'],
                'is_active': True,
            },
        )
        for step in lesson_data['steps']:
            Quest.objects.update_or_create(
                slug=step['slug'],
                defaults={
                    **step,
                    'world': world,
                    'lesson': lesson,
                    'order': step['step_order'],
                    'is_active': True,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_lesson_min_points_required'),
    ]

    operations = [
        migrations.RunPython(align_report_content, migrations.RunPython.noop),
    ]
