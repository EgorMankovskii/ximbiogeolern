from django.db import migrations


QUESTS = {
    'biology': [
        {
            'slug': 'cell-organelle-match',
            'title': 'Клетка: кто за что отвечает',
            'task_type': 'match',
            'difficulty': 1,
            'story': 'Лаборант перепутал подписи к частям клетки. Помогите вернуть каждой структуре ее роль.',
            'theory': 'Ядро хранит наследственную информацию, митохондрии дают клетке энергию, хлоропласты участвуют в фотосинтезе.',
            'starter_code': '',
            'tests': [],
            'content': {
                'pairs': [
                    {'picture': '🧬', 'prompt': 'Ядро клетки', 'answer': 'dna'},
                    {'picture': '⚡', 'prompt': 'Митохондрия', 'answer': 'energy'},
                    {'picture': '🌿', 'prompt': 'Хлоропласт', 'answer': 'photo'},
                ],
                'options': [
                    {'value': 'dna', 'label': 'Хранит ДНК'},
                    {'value': 'energy', 'label': 'Помогает получать энергию'},
                    {'value': 'photo', 'label': 'Участвует в фотосинтезе'},
                ],
            },
            'hint': 'Вспомните: хлоропласт связан с зеленым цветом растений и светом.',
            'easier_text': 'Сначала сопоставьте самый очевидный символ: лист относится к фотосинтезу.',
            'reward_points': 15,
            'visual_kind': 'cell',
            'order': 1,
        },
        {
            'slug': 'chlorophyll-average',
            'title': 'Средний индекс хлорофилла',
            'task_type': 'python',
            'difficulty': 1,
            'story': 'Ботаники измерили индекс хлорофилла у нескольких листьев. Нужно найти среднее значение, чтобы оценить состояние растения.',
            'theory': 'Чем стабильнее показатели хлорофилла, тем проще оценивать здоровье растения по группе листьев.',
            'starter_code': 'def solve(values):\n    # Верните среднее значение списка values.\n    pass\n',
            'tests': [
                {'args': [[10, 12, 14]], 'expected': 12},
                {'args': [[6, 8, 10]], 'expected': 8},
                {'args': [[5]], 'expected': 5},
            ],
            'content': {},
            'hint': 'Среднее = сумма значений / количество значений.',
            'easier_text': 'Список всегда непустой, поэтому деления на ноль здесь не будет.',
            'reward_points': 20,
            'visual_kind': 'leaf-chart',
            'order': 2,
        },
        {
            'slug': 'food-chain-quiz',
            'title': 'Кто производит пищу',
            'task_type': 'quiz',
            'difficulty': 1,
            'story': 'В экосистеме нужно найти организм-продуцент, с которого начинается пищевая цепь.',
            'theory': 'Продуценты создают органические вещества из неорганических. Обычно это растения и водоросли.',
            'starter_code': '',
            'tests': [],
            'content': {
                'correct': 'grass',
                'options': [
                    {'value': 'fox', 'label': 'Лиса'},
                    {'value': 'grass', 'label': 'Трава'},
                    {'value': 'mushroom', 'label': 'Гриб'},
                ],
            },
            'hint': 'Продуцент обычно сам создает питательные вещества с помощью света.',
            'easier_text': 'Выберите организм, который похож на растение.',
            'reward_points': 15,
            'visual_kind': 'ecosystem',
            'order': 3,
        },
        {
            'slug': 'population-growth',
            'title': 'Рост популяции по годам',
            'task_type': 'python',
            'difficulty': 2,
            'story': 'Экологи записали численность вида по годам. Посчитайте, сколько раз численность увеличивалась относительно прошлого года.',
            'theory': 'Такой подсчет помогает быстро увидеть, в какие периоды условия были благоприятными.',
            'starter_code': 'def solve(values):\n    # Посчитайте переходы, где следующее значение больше предыдущего.\n    pass\n',
            'tests': [
                {'args': [[10, 12, 11, 18]], 'expected': 2},
                {'args': [[5, 5, 4]], 'expected': 0},
                {'args': [[1, 2, 3, 4]], 'expected': 3},
            ],
            'content': {},
            'hint': 'Сравнивайте соседние значения: values[i] и values[i + 1].',
            'easier_text': 'Начните со счетчика growth = 0 и увеличивайте его при росте.',
            'reward_points': 35,
            'visual_kind': 'population',
            'order': 4,
        },
    ],
    'chemistry': [
        {
            'slug': 'lab-safety-quiz',
            'title': 'Безопасность в лаборатории',
            'task_type': 'quiz',
            'difficulty': 1,
            'story': 'Перед опытом нужно выбрать правильное действие при работе с веществами.',
            'theory': 'В химии важно не пробовать вещества на вкус, не нюхать напрямую и защищать глаза.',
            'starter_code': '',
            'tests': [],
            'content': {
                'correct': 'glasses',
                'options': [
                    {'value': 'taste', 'label': 'Попробовать вещество'},
                    {'value': 'glasses', 'label': 'Надеть защитные очки'},
                    {'value': 'mix_all', 'label': 'Смешать все реактивы'},
                ],
            },
            'hint': 'Подумайте, что снижает риск для глаз.',
            'easier_text': 'Правильный ответ связан не с реакцией, а с защитой человека.',
            'reward_points': 15,
            'visual_kind': 'lab',
            'order': 1,
        },
        {
            'slug': 'molecule-mass',
            'title': 'Масса молекулы воды',
            'task_type': 'python',
            'difficulty': 1,
            'story': 'Даны атомные массы элементов в молекуле. Напишите Python-функцию, которая находит общую массу.',
            'theory': 'Молекулярная масса равна сумме атомных масс всех атомов в молекуле.',
            'starter_code': 'def solve(atom_masses):\n    # Верните сумму масс атомов.\n    pass\n',
            'tests': [
                {'args': [[1, 1, 16]], 'expected': 18},
                {'args': [[12, 16, 16]], 'expected': 44},
                {'args': [[23, 35]], 'expected': 58},
            ],
            'content': {},
            'hint': 'В Python список можно сложить функцией sum(atom_masses).',
            'easier_text': 'Для воды H2O массы можно представить как [1, 1, 16].',
            'reward_points': 20,
            'visual_kind': 'molecule',
            'order': 2,
        },
        {
            'slug': 'formula-match',
            'title': 'Формулы и вещества',
            'task_type': 'match',
            'difficulty': 1,
            'story': 'Сопоставьте формулы с привычными названиями веществ.',
            'theory': 'Формулы показывают, какие атомы входят в состав вещества и в каком количестве.',
            'starter_code': '',
            'tests': [],
            'content': {
                'pairs': [
                    {'picture': 'H₂O', 'prompt': 'H₂O', 'answer': 'water'},
                    {'picture': 'CO₂', 'prompt': 'CO₂', 'answer': 'carbon'},
                    {'picture': 'NaCl', 'prompt': 'NaCl', 'answer': 'salt'},
                ],
                'options': [
                    {'value': 'water', 'label': 'Вода'},
                    {'value': 'carbon', 'label': 'Углекислый газ'},
                    {'value': 'salt', 'label': 'Поваренная соль'},
                ],
            },
            'hint': 'NaCl часто встречается на кухне.',
            'easier_text': 'Начните с H₂O: это самая известная формула воды.',
            'reward_points': 15,
            'visual_kind': 'formula',
            'order': 3,
        },
        {
            'slug': 'reaction-balance',
            'title': 'Хватит ли реагентов',
            'task_type': 'python',
            'difficulty': 2,
            'story': 'Для реакции известны нужные количества веществ и запасы в лаборатории. Проверьте, можно ли провести опыт.',
            'theory': 'Реакция возможна, если каждого реагента в наличии не меньше, чем требуется.',
            'starter_code': 'def solve(required, available):\n    # Верните True, если всех реагентов достаточно.\n    pass\n',
            'tests': [
                {'args': [{'H': 2, 'O': 1}, {'H': 3, 'O': 1}], 'expected': True},
                {'args': [{'C': 1, 'O': 2}, {'C': 1, 'O': 1}], 'expected': False},
                {'args': [{}, {'Na': 1}], 'expected': True},
            ],
            'content': {},
            'hint': 'Используйте available.get(name, 0), чтобы отсутствующий реагент считался нулем.',
            'easier_text': 'Если нашли хотя бы один нехватающий реагент, сразу возвращайте False.',
            'reward_points': 35,
            'visual_kind': 'reaction',
            'order': 4,
        },
    ],
    'geography': [
        {
            'slug': 'map-symbols-match',
            'title': 'Условные знаки карты',
            'task_type': 'match',
            'difficulty': 1,
            'story': 'Карта потеряла легенду. Сопоставьте значки с объектами местности.',
            'theory': 'Легенда карты объясняет условные обозначения: реки, горы, города и дороги.',
            'starter_code': '',
            'tests': [],
            'content': {
                'pairs': [
                    {'picture': '〰️', 'prompt': 'Синяя извилистая линия', 'answer': 'river'},
                    {'picture': '▲', 'prompt': 'Треугольник на карте', 'answer': 'mountain'},
                    {'picture': '●', 'prompt': 'Крупная точка', 'answer': 'city'},
                ],
                'options': [
                    {'value': 'river', 'label': 'Река'},
                    {'value': 'mountain', 'label': 'Гора'},
                    {'value': 'city', 'label': 'Город'},
                ],
            },
            'hint': 'Извилистая линия чаще всего показывает воду.',
            'easier_text': 'Начните с треугольника: им часто обозначают вершины и горы.',
            'reward_points': 15,
            'visual_kind': 'map',
            'order': 1,
        },
        {
            'slug': 'highest-point',
            'title': 'Самая высокая точка маршрута',
            'task_type': 'python',
            'difficulty': 1,
            'story': 'Географы измерили высоты точек маршрута. Напишите функцию, которая найдет максимальную высоту.',
            'theory': 'Максимальная высота помогает оценить сложность маршрута и выбрать обзорную точку.',
            'starter_code': 'def solve(heights):\n    # Верните максимальную высоту.\n    pass\n',
            'tests': [
                {'args': [[120, 340, 210]], 'expected': 340},
                {'args': [[-5, 0, 12]], 'expected': 12},
                {'args': [[77]], 'expected': 77},
            ],
            'content': {},
            'hint': 'В Python есть функция max.',
            'easier_text': 'Список heights всегда непустой.',
            'reward_points': 20,
            'visual_kind': 'terrain',
            'order': 2,
        },
        {
            'slug': 'climate-zone-quiz',
            'title': 'Климатическая зона',
            'task_type': 'quiz',
            'difficulty': 1,
            'story': 'Выберите природную зону, где круглый год жарко и часто идут дожди.',
            'theory': 'Влажные экваториальные леса формируются в жарком и очень влажном климате.',
            'starter_code': '',
            'tests': [],
            'content': {
                'correct': 'rainforest',
                'options': [
                    {'value': 'tundra', 'label': 'Тундра'},
                    {'value': 'rainforest', 'label': 'Влажный экваториальный лес'},
                    {'value': 'desert', 'label': 'Пустыня'},
                ],
            },
            'hint': 'Ищите вариант, где много тепла и влаги.',
            'easier_text': 'Пустыня сухая, тундра холодная.',
            'reward_points': 15,
            'visual_kind': 'climate',
            'order': 3,
        },
        {
            'slug': 'route-distance',
            'title': 'Длина маршрута на прямой',
            'task_type': 'python',
            'difficulty': 2,
            'story': 'Навигатор получил отметки точек на одной линии. Посчитайте общий путь между соседними точками.',
            'theory': 'Общий путь складывается из расстояний между каждой парой соседних точек.',
            'starter_code': 'def solve(points):\n    # Верните сумму расстояний между соседними точками.\n    pass\n',
            'tests': [
                {'args': [[0, 3, 7]], 'expected': 7},
                {'args': [[10, 4, 4, 1]], 'expected': 9},
                {'args': [[5]], 'expected': 0},
            ],
            'content': {},
            'hint': 'Для расстояния используйте abs(points[i + 1] - points[i]).',
            'easier_text': 'Если точка одна, путь равен 0.',
            'reward_points': 35,
            'visual_kind': 'route',
            'order': 4,
        },
    ],
}


def upsert_richer_quests(apps, schema_editor):
    World = apps.get_model('main', 'World')
    Quest = apps.get_model('main', 'Quest')

    for world_slug, quests in QUESTS.items():
        world = World.objects.get(slug=world_slug)
        for quest in quests:
            Quest.objects.update_or_create(
                slug=quest['slug'],
                defaults={**quest, 'world': world, 'is_active': True},
            )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_quest_content_quest_task_type_and_more'),
    ]

    operations = [
        migrations.RunPython(upsert_richer_quests, migrations.RunPython.noop),
    ]
