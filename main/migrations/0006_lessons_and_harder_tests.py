from django.db import migrations


LESSONS = {
    'biology': {
        'slug': 'ecosystem-and-cells',
        'title': 'Клетки и экосистемы',
        'intro': 'Разберитесь, как устроена клетка, как работает пищевая цепь и как Python помогает анализировать биологические наблюдения.',
        'quest_slugs': [
            'cell-organelle-match',
            'food-chain-quiz',
            'chlorophyll-average',
            'population-growth',
        ],
    },
    'chemistry': {
        'slug': 'lab-and-formulas',
        'title': 'Лаборатория и формулы',
        'intro': 'Сначала проверьте понимание химической безопасности и формул, затем используйте Python для расчетов вещества и реагентов.',
        'quest_slugs': [
            'lab-safety-quiz',
            'formula-match',
            'molecule-mass',
            'reaction-balance',
        ],
    },
    'geography': {
        'slug': 'maps-climate-routes',
        'title': 'Карты, климат и маршруты',
        'intro': 'Пройдите от чтения карты и анализа климата к Python-задачам про высоты и расстояния.',
        'quest_slugs': [
            'map-symbols-match',
            'climate-zone-quiz',
            'highest-point',
            'route-distance',
        ],
    },
}


HARDER_UPDATES = {
    'food-chain-quiz': {
        'title': 'Пищевая цепь после засухи',
        'difficulty': 2,
        'story': 'В экосистеме стало меньше травы. Какое последствие наиболее вероятно для всей пищевой цепи?',
        'theory': 'Продуценты находятся в основании пищевой цепи. Если их становится меньше, энергии получает меньше вся цепь потребителей.',
        'content': {
            'correct': 'less_consumers',
            'options': [
                {'value': 'more_predators', 'label': 'Хищников сразу станет больше, потому что добычу легче найти'},
                {'value': 'less_consumers', 'label': 'Численность травоядных может снизиться, а затем пострадают хищники'},
                {'value': 'no_effect', 'label': 'Изменение травы не влияет на животных'},
                {'value': 'only_mushrooms', 'label': 'Изменятся только грибы, остальные организмы не связаны'},
            ],
        },
        'hint': 'Подумайте, кто получает энергию от растений первым.',
        'easier_text': 'Если меньше еды у травоядных, дальше меняется и положение хищников.',
    },
    'lab-safety-quiz': {
        'title': 'Что делать при неизвестном запахе',
        'difficulty': 2,
        'story': 'При нагревании вещества появился резкий запах. Как поступить безопаснее всего?',
        'theory': 'В химии нельзя нюхать вещества напрямую. Запах проверяют только осторожным направлением паров рукой и только по указанию учителя.',
        'content': {
            'correct': 'stop_teacher',
            'options': [
                {'value': 'direct_smell', 'label': 'Наклониться ближе и понюхать напрямую'},
                {'value': 'stop_teacher', 'label': 'Остановить нагрев и сообщить учителю'},
                {'value': 'add_water', 'label': 'Сразу добавить воду в пробирку'},
                {'value': 'close_with_hand', 'label': 'Плотно закрыть пробирку рукой'},
            ],
        },
        'hint': 'Безопасное действие сначала уменьшает риск, а не продолжает опыт.',
        'easier_text': 'Если запах неизвестный, лучше прекратить действие и позвать взрослого/учителя.',
    },
    'climate-zone-quiz': {
        'title': 'Климат по данным наблюдений',
        'difficulty': 2,
        'story': 'Даны признаки: высокая температура весь год, осадки почти каждый месяц, много вечнозеленых растений. Какая природная зона подходит лучше всего?',
        'theory': 'Климатическую зону определяют не по одному признаку, а по сочетанию температуры, осадков и растительности.',
        'content': {
            'correct': 'rainforest',
            'options': [
                {'value': 'savanna', 'label': 'Саванна: жарко, но есть выраженный сухой сезон'},
                {'value': 'rainforest', 'label': 'Влажный экваториальный лес: жарко и влажно круглый год'},
                {'value': 'steppe', 'label': 'Степь: умеренный климат и мало деревьев'},
                {'value': 'tundra', 'label': 'Тундра: холодно, короткое лето, мхи и лишайники'},
            ],
        },
        'hint': 'Ключевой признак — осадки почти каждый месяц.',
        'easier_text': 'Ищите вариант без сухого сезона и без холода.',
    },
    'cell-organelle-match': {
        'difficulty': 2,
        'content': {
            'pairs': [
                {'picture': '🧬', 'prompt': 'Структура управляет работой клетки и хранит наследственную информацию', 'answer': 'nucleus'},
                {'picture': '⚡', 'prompt': 'Органоид активно участвует в клеточном дыхании', 'answer': 'mitochondria'},
                {'picture': '🌿', 'prompt': 'Органоид есть у растений и связан с образованием глюкозы на свету', 'answer': 'chloroplast'},
                {'picture': '🧱', 'prompt': 'Жесткая оболочка поддерживает форму растительной клетки', 'answer': 'wall'},
            ],
            'options': [
                {'value': 'nucleus', 'label': 'Ядро'},
                {'value': 'mitochondria', 'label': 'Митохондрия'},
                {'value': 'chloroplast', 'label': 'Хлоропласт'},
                {'value': 'wall', 'label': 'Клеточная стенка'},
            ],
        },
    },
    'formula-match': {
        'difficulty': 2,
        'content': {
            'pairs': [
                {'picture': 'CaCO₃', 'prompt': 'Основной компонент известняка и мела', 'answer': 'limestone'},
                {'picture': 'NaHCO₃', 'prompt': 'Пищевая сода, выделяет CO₂ при реакции с кислотой', 'answer': 'soda'},
                {'picture': 'HCl', 'prompt': 'Кислота, содержащаяся в желудочном соке', 'answer': 'acid'},
                {'picture': 'NH₃', 'prompt': 'Газ с резким запахом, раствор называют нашатырным спиртом', 'answer': 'ammonia'},
            ],
            'options': [
                {'value': 'limestone', 'label': 'Карбонат кальция'},
                {'value': 'soda', 'label': 'Гидрокарбонат натрия'},
                {'value': 'acid', 'label': 'Соляная кислота'},
                {'value': 'ammonia', 'label': 'Аммиак'},
            ],
        },
    },
    'map-symbols-match': {
        'difficulty': 2,
        'content': {
            'pairs': [
                {'picture': '〰️', 'prompt': 'Линия идет по низинам и соединяется с озером', 'answer': 'river'},
                {'picture': '▲', 'prompt': 'Рядом подписана абсолютная высота 1642 м', 'answer': 'peak'},
                {'picture': '— —', 'prompt': 'Линия соединяет населенные пункты и пересекает мост', 'answer': 'road'},
                {'picture': '▦', 'prompt': 'Площадной знак с кварталами и улицами', 'answer': 'city'},
            ],
            'options': [
                {'value': 'river', 'label': 'Река'},
                {'value': 'peak', 'label': 'Горная вершина'},
                {'value': 'road', 'label': 'Дорога'},
                {'value': 'city', 'label': 'Населенный пункт'},
            ],
        },
    },
}


def create_lessons_and_update_quests(apps, schema_editor):
    World = apps.get_model('main', 'World')
    Lesson = apps.get_model('main', 'Lesson')
    Quest = apps.get_model('main', 'Quest')

    for world_slug, lesson_data in LESSONS.items():
        world = World.objects.get(slug=world_slug)
        lesson, _ = Lesson.objects.update_or_create(
            world=world,
            slug=lesson_data['slug'],
            defaults={
                'title': lesson_data['title'],
                'intro': lesson_data['intro'],
                'order': 1,
                'is_active': True,
            },
        )
        for index, quest_slug in enumerate(lesson_data['quest_slugs'], start=1):
            Quest.objects.filter(slug=quest_slug).update(lesson=lesson, step_order=index, order=index)

    for quest_slug, data in HARDER_UPDATES.items():
        Quest.objects.filter(slug=quest_slug).update(**data)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_quest_options_quest_step_order_lesson_and_more'),
    ]

    operations = [
        migrations.RunPython(create_lessons_and_update_quests, migrations.RunPython.noop),
    ]
