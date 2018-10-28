from django.test import TestCase
from django.utils import timezone

from mosta.base.testutils import generators
from mosta.dashboard.utils import dashboard_utils


class TestDashboardUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = generators.generate_test_user()

    def test_get_average_call_duration(self):
        phone = generators.generate_phone(self.user)
        sim = generators.generate_sim(self.user, phone)
        now = timezone.now()
        generators.generate_calling_history(self.user, sim, now, 5, [10, 20, 30, 40, 50])

        expected = 1800  # 30 minutes in seconds
        actual = dashboard_utils.get_average_call_duration(self.user, now)
        self.assertEqual(expected, actual)

    def test_get_average_call_duration_no_history(self):
        now = timezone.now()
        actual = dashboard_utils.get_average_call_duration(self.user, now)

        self.assertEqual(0, actual)

    def test_get_average_call_duration_single_history(self):
        phone = generators.generate_phone(self.user)
        sim = generators.generate_sim(self.user, phone)
        now = timezone.now()
        generators.generate_calling_history(self.user, sim, now, 1, [10])

        expected = 600  # 10 minutes in seconds
        actual = dashboard_utils.get_average_call_duration(self.user, now)
        self.assertEqual(expected, actual)

    def test_get_average_call_duration_filtered_by_sim(self):
        phone = generators.generate_phone(self.user)
        sim = generators.generate_sim(self.user, phone)
        now = timezone.now()
        generators.generate_calling_history(self.user, sim, now, 10)

        relevant_sim = generators.generate_sim(self.user, phone)
        generators.generate_calling_history(self.user, relevant_sim, now, 5, [10, 20, 30, 40, 50])

        expected = 1800  # 30 minutes in seconds
        actual = dashboard_utils.get_average_call_duration(self.user, now, sim=relevant_sim)
        self.assertEqual(expected, actual)
