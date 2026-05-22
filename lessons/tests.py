from django.test import TestCase

from .services import check_solution


class CheckSolutionTests(TestCase):
    """Тесты сервиса проверки решений.

    Они не проверяют внешний вид сайта, зато страхуют самую важную часть:
    корректный код должен проходить, ошибка должна возвращать понятный feedback.
    """

    def test_successful_solution_passes_all_tests(self):
        result = check_solution(
            'def solve(a, b):\n    return a + b\n',
            [{'args': [2, 3], 'expected': 5}],
        )

        self.assertTrue(result.is_success)
        self.assertEqual(result.passed_tests, 1)

    def test_wrong_answer_returns_feedback(self):
        result = check_solution(
            'def solve(a, b):\n    return a - b\n',
            [{'args': [2, 3], 'expected': 5}],
        )

        self.assertFalse(result.is_success)
        self.assertIn('ожидали', result.feedback)

    def test_imports_are_blocked(self):
        result = check_solution(
            'import os\n\ndef solve():\n    return 1\n',
            [{'args': [], 'expected': 1}],
        )

        self.assertFalse(result.is_success)
        self.assertIn('Импорт', result.feedback)

    def test_endless_loop_times_out(self):
        result = check_solution(
            'def solve():\n    while True:\n        pass\n',
            [{'args': [], 'expected': 1}],
        )

        self.assertFalse(result.is_success)
        self.assertIn('дольше 2 секунд', result.feedback)

# Create your tests here.
