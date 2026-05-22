import ast
import base64
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class CheckResult:
    """Единый формат результата автопроверки."""

    is_success: bool
    passed_tests: int
    total_tests: int
    feedback: str


class UnsafeCodeError(Exception):
    """Ошибка для кода, который нельзя запускать даже в учебной песочнице."""


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
    """Быстрая проверка кода перед запуском.

    Это не промышленная изоляция, но хороший учебный предохранитель: запрещаем
    импорт модулей, чтение файлов и динамическое выполнение строк как кода.
    """

    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise UnsafeCodeError('Импорт модулей отключен в учебной песочнице.')
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_NAMES:
                raise UnsafeCodeError(f'Функция {node.func.id} запрещена.')


def check_solution(code, tests):
    """Проверяет функцию solve(...) на JSON-тестах задачи.

    Каждый тест выглядит так: {"args": [1, 2], "expected": 3}. Значения из
    args передаются в solve как позиционные аргументы.
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
import math
import sys

SAFE_BUILTINS = {
    'abs': abs, 'all': all, 'any': any, 'bool': bool, 'dict': dict,
    'enumerate': enumerate, 'filter': filter, 'float': float, 'int': int,
    'len': len, 'list': list, 'map': map, 'max': max, 'min': min, 'pow': pow,
    'print': print, 'range': range, 'reversed': reversed, 'round': round,
    'set': set, 'sorted': sorted, 'str': str, 'sum': sum, 'tuple': tuple,
    'zip': zip, 'exp': math.exp, 'log': math.log,
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
message = ''
tests = data['tests']
for index, test in enumerate(tests, start=1):
    args = test.get('args', [])
    expected = test.get('expected')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            actual = solve(*args)
    except Exception as error:
        message = f'Тест {index}: решение упало с ошибкой {error}.'
        break

    if actual == expected:
        passed += 1
    else:
        message = f'Тест {index}: ожидали {expected!r}, получили {actual!r}.'
        break

print(json.dumps({'kind': 'result', 'passed': passed, 'total': len(tests), 'message': message}))
"""

    command = [sys.executable, '-c', runner, payload]
    if os.getenv('EDUQUEST_SANDBOX') == 'docker':
        # Режим для архитектуры из отчета: пользовательский код запускается в
        # отдельном контейнере без сети, с ограничением памяти и CPU.
        command = [
            'docker',
            'run',
            '--rm',
            '--network',
            'none',
            '--memory',
            '128m',
            '--cpus',
            '0.5',
            'python:3.14-slim',
            'python',
            '-c',
            runner,
            payload,
        ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            encoding='utf-8',
            timeout=2,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CheckResult(False, 0, len(tests), 'Код выполнялся дольше 2 секунд. Попробуйте упростить решение.')

    if not completed.stdout:
        return CheckResult(False, 0, len(tests), 'Проверка не смогла получить результат выполнения.')

    data = json.loads(completed.stdout.strip().splitlines()[-1])
    if data['kind'] == 'startup_error':
        return CheckResult(False, 0, len(tests), f"Код упал при запуске: {data['message']}.")
    if data['kind'] == 'missing_solve':
        return CheckResult(False, 0, len(tests), 'Нужна функция solve(...), которая возвращает ответ.')

    if data['passed'] == data['total']:
        return CheckResult(True, data['passed'], data['total'], 'Квест пройден. Данные экспедиции подтверждены!')

    return CheckResult(False, data['passed'], data['total'], data['message'])
