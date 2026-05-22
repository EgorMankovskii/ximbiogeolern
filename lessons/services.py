import ast
import base64
import json
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class CheckResult:
    """Результат проверки решения.

    Dataclass удобен здесь тем, что view получает понятный объект вместо
    словаря с неочевидными ключами.
    """

    is_success: bool
    passed_tests: int
    total_tests: int
    feedback: str


class UnsafeCodeError(Exception):
    """Исключение для кода, который запрещен в учебной песочнице."""


FORBIDDEN_NAMES = {
    '__import__',
    'compile',
    'eval',
    'exec',
    'globals',
    'locals',
    'open',
    'input',
}

def _validate_code(code):
    """Проверяет код до запуска.

    Это не промышленная sandbox-защита, а учебный предохранитель: блокируем
    импорт модулей, работу с файлами и динамическое выполнение кода.
    """

    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise UnsafeCodeError('Импорт модулей в этой песочнице отключен.')
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_NAMES:
                raise UnsafeCodeError(f'Функция {node.func.id} запрещена.')


def check_solution(code, tests):
    """Запускает решение на тестах задачи.

    Ожидается, что ученик напишет функцию solve(...). Каждый тест содержит
    args и expected. Например: {"args": [2, 3], "expected": 5}.
    """

    try:
        _validate_code(code)
    except SyntaxError as error:
        return CheckResult(False, 0, len(tests), f'Синтаксическая ошибка: {error.msg}.')
    except UnsafeCodeError as error:
        return CheckResult(False, 0, len(tests), str(error))

    payload = base64.b64encode(json.dumps({'code': code, 'tests': tests}).encode()).decode()
    runner = r"""
import base64
import contextlib
import io
import json
import sys

SAFE_BUILTINS = {
    'abs': abs, 'all': all, 'any': any, 'bool': bool, 'dict': dict,
    'enumerate': enumerate, 'filter': filter, 'float': float, 'int': int,
    'len': len, 'list': list, 'map': map, 'max': max, 'min': min, 'pow': pow,
    'print': print, 'range': range, 'reversed': reversed, 'round': round,
    'set': set, 'sorted': sorted, 'str': str, 'sum': sum, 'tuple': tuple,
    'zip': zip,
}

data = json.loads(base64.b64decode(sys.argv[1]).decode())
namespace = {'__builtins__': SAFE_BUILTINS}

try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(data['code'], namespace)
except Exception as error:
    print(json.dumps({'kind': 'startup_error', 'message': str(error)}))
    raise SystemExit

solve = namespace.get('solve')
if not callable(solve):
    print(json.dumps({'kind': 'missing_solve'}))
    raise SystemExit

passed = 0
first_error = ''
tests = data['tests']
for index, test in enumerate(tests, start=1):
    args = test.get('args', [])
    expected = test.get('expected')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            actual = solve(*args)
    except Exception as error:
        first_error = f'Тест {index}: решение упало с ошибкой {error}.'
        break

    if actual == expected:
        passed += 1
    else:
        first_error = f'Тест {index}: ожидали {expected!r}, получили {actual!r}.'
        break

print(json.dumps({'kind': 'result', 'passed': passed, 'total': len(tests), 'message': first_error}))
"""

    try:
        completed = subprocess.run(
            [sys.executable, '-c', runner, payload],
            capture_output=True,
            encoding='utf-8',
            timeout=2,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CheckResult(False, 0, len(tests), 'Проверка остановлена: код выполнялся дольше 2 секунд.')

    if not completed.stdout:
        return CheckResult(False, 0, len(tests), 'Проверка не смогла получить результат от кода.')

    data = json.loads(completed.stdout.strip().splitlines()[-1])
    if data['kind'] == 'startup_error':
        return CheckResult(False, 0, len(tests), f"Код упал при запуске: {data['message']}.")
    if data['kind'] == 'missing_solve':
        return CheckResult(False, 0, len(tests), 'Нужна функция solve(...), которая возвращает ответ.')

    passed = data['passed']
    total = data['total']

    if passed == total:
        return CheckResult(True, passed, total, 'Отлично, все тесты пройдены.')

    return CheckResult(False, passed, total, data['message'])


def recommend_difficulty(success_rate):
    """Подбирает следующий уровень по успехам ученика."""

    if success_rate >= 75:
        return 3
    if success_rate >= 40:
        return 2
    return 1
