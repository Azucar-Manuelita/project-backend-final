from datetime import date

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from gym_core.models import GymUser, Goal, TrainingPlan


class AdminUsersListTestCase(APITestCase):

    def setUp(self):
        self.admin_user = GymUser.objects.create_user(
            username="admin_user",
            email="admin@gym.com",
            password="AdminPass123",
            is_staff=True,
        )

        self.user_with_active_plan = GymUser.objects.create_user(
            username="active_user",
            email="active@gym.com",
            password="UserPass123",
        )

        self.user_without_plan = GymUser.objects.create_user(
            username="inactive_user",
            email="inactive@gym.com",
            password="UserPass123",
        )

        self.goal = Goal.objects.create(
            name="Hipertrofia",
            description="Ganancia de masa muscular",
        )

        TrainingPlan.objects.create(
            user=self.user_with_active_plan,
            goal=self.goal,
            weekly_frequency=4,
            duration_weeks=8,
            start_date=date.today(),
            status="active",
        )

        self.url = reverse("admin-users-list")

    def test_admin_can_view_users_list_with_correct_plan_status(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        data = response.data["data"]

        active_entry = next(
            item for item in data if item["username"] == "active_user"
        )
        inactive_entry = next(
            item for item in data if item["username"] == "inactive_user"
        )

        self.assertEqual(active_entry["plan_status"], "Active")
        self.assertEqual(inactive_entry["plan_status"], "Inactive")

    def test_non_admin_user_receives_forbidden(self):
        self.client.force_authenticate(user=self.user_without_plan)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)