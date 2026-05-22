from django.test import Client, TestCase
from django.urls import resolve
from django.contrib.auth import get_user_model

from .checker import check_solution
from . import views
from .models import Lesson, Progress, Quest, Submission, World


class EduQuestCheckerTests(TestCase):
    """Минимальные тесты автопроверки EduQuest."""

    def test_correct_solution_passes(self):
        result = check_solution(
            'def solve(values):\n    return sum(values)\n',
            [{'args': [[1, 2, 3]], 'expected': 6}],
        )

        self.assertTrue(result.is_success)
        self.assertEqual(result.passed_tests, 1)

    def test_wrong_solution_returns_feedback(self):
        result = check_solution(
            'def solve(values):\n    return 0\n',
            [{'args': [[1, 2, 3]], 'expected': 6}],
        )

        self.assertFalse(result.is_success)
        self.assertEqual(result.passed_tests, 0)

    def test_import_is_blocked(self):
        result = check_solution(
            'import os\n\ndef solve(values):\n    return 1\n',
            [{'args': [[1]], 'expected': 1}],
        )

        self.assertFalse(result.is_success)


class EduQuestReportFlowTests(TestCase):
    """Проверки сценариев, которые описаны в отчете по практике."""

    def test_database_uses_report_world_names(self):
        self.assertTrue(World.objects.filter(title='Био-купол').exists())
        self.assertTrue(World.objects.filter(title='Квантовая лаборатория').exists())
        self.assertTrue(World.objects.filter(title='Глобальная карта').exists())

    def test_advanced_lesson_is_locked_without_research_points(self):
        lesson = Lesson.objects.get(slug='population-simulation')

        self.assertGreater(lesson.min_points_required, 0)

    def test_biology_module_has_ten_active_research_lessons(self):
        biology = World.objects.get(slug='biology')
        active_lessons = Lesson.objects.filter(world=biology, is_active=True)

        self.assertEqual(active_lessons.count(), 10)
        self.assertTrue(active_lessons.filter(slug='dna-sequence-research').exists())
        self.assertTrue(active_lessons.filter(slug='phenotype-prediction').exists())
        self.assertTrue(active_lessons.filter(theme='Биоинформатика').exists())

    def test_dna_sequence_analysis_step_passes(self):
        quest = Quest.objects.get(slug='dna-sequence-analysis')
        code = (
            'def solve(dna):\n'
            '    counts = {"A": 0, "T": 0, "C": 0, "G": 0}\n'
            '    for letter in dna:\n'
            '        counts[letter] += 1\n'
            '    gc = round(((counts["G"] + counts["C"]) / len(dna) * 100) if dna else 0, 2)\n'
            '    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}\n'
            '    found = set()\n'
            '    for size in range(4, len(dna) + 1):\n'
            '        for start in range(0, len(dna) - size + 1):\n'
            '            part = dna[start:start + size]\n'
            '            reverse_complement = ""\n'
            '            for letter in reversed(part):\n'
            '                reverse_complement += complement[letter]\n'
            '            if part == reverse_complement:\n'
            '                found.add(part)\n'
            '    return {"counts": counts, "gc_percent": gc, "palindromes": sorted(found)}\n'
        )

        result = check_solution(code, quest.tests)

        self.assertTrue(result.is_success)
        self.assertEqual(result.passed_tests, 3)

    def test_ecosystem_shannon_step_can_use_log_builtin(self):
        quest = Quest.objects.get(slug='ecosystem-shannon-index')
        code = (
            'def solve(rows):\n'
            '    zones = {}\n'
            '    for row in rows:\n'
            '        zone = row["zone"]\n'
            '        species = row["species"]\n'
            '        zones.setdefault(zone, {})[species] = row["count"]\n'
            '    shannon = {}\n'
            '    dominant = {}\n'
            '    for zone, species_counts in zones.items():\n'
            '        total = sum(species_counts.values())\n'
            '        value = 0\n'
            '        best_species = None\n'
            '        best_count = -1\n'
            '        for species, count in species_counts.items():\n'
            '            p = count / total\n'
            '            value += -p * log(p, 2)\n'
            '            if count > best_count:\n'
            '                best_species = species\n'
            '                best_count = count\n'
            '        shannon[zone] = round(value, 3)\n'
            '        dominant[zone] = best_species\n'
            '    return {"shannon": shannon, "dominant": dominant}\n'
        )

        result = check_solution(code, quest.tests)

        self.assertTrue(result.is_success)
        self.assertEqual(result.passed_tests, 2)

    def test_reset_progress_removes_current_session_only(self):
        client = Client()
        session = client.session
        session['started'] = True
        session.save()
        session_key = session.session_key
        quest = Quest.objects.get(slug='dna-palindrome-quiz')
        Submission.objects.create(
            quest=quest,
            session_key=session_key,
            code='gc_and_palindromes',
            is_success=True,
            passed_tests=1,
            total_tests=1,
            feedback='ok',
        )
        Progress.objects.create(session_key=session_key, world=quest.world, points=25, solved_count=1)

        self.assertEqual(Submission.objects.filter(session_key=session_key).count(), 1)
        self.assertEqual(Progress.objects.filter(session_key=session_key).count(), 1)

        client.post('/progress/reset/', {'confirm_reset': 'RESET'})

        self.assertEqual(Submission.objects.filter(session_key=session_key).count(), 0)
        self.assertEqual(Progress.objects.filter(session_key=session_key).count(), 0)

    def test_career_and_textbooks_pages_open(self):
        self.assertEqual(resolve('/career/').func, views.career_view)
        self.assertEqual(resolve('/textbooks/').func, views.textbooks_view)
        self.assertEqual(resolve('/textbooks/python-dlya-nauchnyh-zadach/').func, views.textbook_detail)
        self.assertEqual(
            resolve('/textbooks/python-dlya-nauchnyh-zadach/funkciya-solve-i-avtoproverka/').func,
            views.textbook_topic_detail,
        )

    def test_career_upgrade_is_saved_in_session(self):
        client = Client()
        session = client.session
        session['started'] = True
        session.save()
        session_key = session.session_key
        chemistry = World.objects.get(slug='chemistry')
        Progress.objects.create(session_key=session_key, world=chemistry, points=90, solved_count=2)

        response = client.post('/career/', {'upgrade_id': 'coat'})

        self.assertEqual(response.status_code, 302)
        self.assertIn('coat', client.session.get('chemist_upgrades', []))

    def test_studio_rejects_non_staff_users(self):
        user_model = get_user_model()
        user_model.objects.create_user('plain-user', password='StrongPass123')
        client = Client()

        response = client.post('/admin/login/', {'username': 'plain-user', 'password': 'StrongPass123'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'нет доступа')
        self.assertEqual(client.get('/admin/').status_code, 302)

    def test_studio_staff_user_can_open_admin_panel(self):
        user_model = get_user_model()
        user_model.objects.create_user('staff-user', password='StrongPass123', is_staff=True)
        client = Client()

        response = client.post('/admin/login/', {'username': 'staff-user', 'password': 'StrongPass123'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(client.get('/admin/').status_code, 200)
