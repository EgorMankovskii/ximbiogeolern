from django.db import migrations


EXERCISES = [
    {
        'title': 'Сумма двух чисел',
        'slug': 'sum-two-numbers',
        'topic': 'Функции',
        'difficulty': 1,
        'short_description': 'Разминка: вернуть сумму двух аргументов.',
        'task_text': 'Напишите функцию solve(a, b), которая возвращает сумму чисел a и b.',
        'starter_code': 'def solve(a, b):\n    # Верните сумму двух чисел.\n    pass\n',
        'tests': [
            {'args': [2, 3], 'expected': 5},
            {'args': [-4, 10], 'expected': 6},
            {'args': [0, 0], 'expected': 0},
        ],
    },
    {
        'title': 'Количество четных',
        'slug': 'count-even',
        'topic': 'Списки',
        'difficulty': 1,
        'short_description': 'Посчитать, сколько чисел в списке делятся на два.',
        'task_text': 'Напишите solve(numbers), которая возвращает количество четных чисел в списке numbers.',
        'starter_code': 'def solve(numbers):\n    # Пройдите по списку и посчитайте четные элементы.\n    pass\n',
        'tests': [
            {'args': [[1, 2, 3, 4]], 'expected': 2},
            {'args': [[7, 9, 11]], 'expected': 0},
            {'args': [[0, -2, 5, 8]], 'expected': 3},
        ],
    },
    {
        'title': 'Слова длиннее N',
        'slug': 'words-longer-than-n',
        'topic': 'Строки',
        'difficulty': 2,
        'short_description': 'Отфильтровать слова по длине и сохранить порядок.',
        'task_text': 'Напишите solve(words, n), которая возвращает список слов длиной строго больше n.',
        'starter_code': 'def solve(words, n):\n    # Верните новый список, не меняя исходный.\n    pass\n',
        'tests': [
            {'args': [['кот', 'питон', 'код'], 3], 'expected': ['питон']},
            {'args': [['alpha', 'go', 'django'], 4], 'expected': ['alpha', 'django']},
            {'args': [[], 2], 'expected': []},
        ],
    },
    {
        'title': 'Частотный словарь',
        'slug': 'frequency-map',
        'topic': 'Словари',
        'difficulty': 2,
        'short_description': 'Собрать словарь: элемент -> количество повторений.',
        'task_text': 'Напишите solve(items), которая возвращает словарь с количеством повторений каждого элемента.',
        'starter_code': 'def solve(items):\n    result = {}\n    # Заполните словарь result.\n    return result\n',
        'tests': [
            {'args': [['a', 'b', 'a']], 'expected': {'a': 2, 'b': 1}},
            {'args': [['x', 'x', 'y', 'z', 'z', 'z']], 'expected': {'x': 2, 'y': 1, 'z': 3}},
            {'args': [[]], 'expected': {}},
        ],
    },
    {
        'title': 'Сжатие повторов',
        'slug': 'compress-runs',
        'topic': 'Алгоритмы',
        'difficulty': 3,
        'short_description': 'Свернуть подряд идущие одинаковые значения в пары.',
        'task_text': 'Напишите solve(items), которая возвращает список пар [значение, количество] для подряд идущих повторов.',
        'starter_code': 'def solve(items):\n    # Пример: [1, 1, 2] -> [[1, 2], [2, 1]]\n    pass\n',
        'tests': [
            {'args': [[1, 1, 2, 2, 2, 3]], 'expected': [[1, 2], [2, 3], [3, 1]]},
            {'args': [['a', 'a', 'b', 'a']], 'expected': [['a', 2], ['b', 1], ['a', 1]]},
            {'args': [[]], 'expected': []},
        ],
    },
    {
        'title': 'Первый неповторяющийся символ',
        'slug': 'first-unique-char',
        'topic': 'Алгоритмы',
        'difficulty': 3,
        'short_description': 'Найти первый символ строки, который встречается ровно один раз.',
        'task_text': 'Напишите solve(text), которая возвращает первый неповторяющийся символ. Если такого нет, верните None.',
        'starter_code': 'def solve(text):\n    # Подумайте, как не потерять порядок символов.\n    pass\n',
        'tests': [
            {'args': ['abracadabra'], 'expected': 'c'},
            {'args': ['aabbcc'], 'expected': None},
            {'args': ['python'], 'expected': 'p'},
        ],
    },
]


def seed_exercises(apps, schema_editor):
    Exercise = apps.get_model('lessons', 'Exercise')
    for data in EXERCISES:
        Exercise.objects.update_or_create(slug=data['slug'], defaults=data)


def remove_exercises(apps, schema_editor):
    Exercise = apps.get_model('lessons', 'Exercise')
    Exercise.objects.filter(slug__in=[item['slug'] for item in EXERCISES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_exercises, remove_exercises),
    ]
