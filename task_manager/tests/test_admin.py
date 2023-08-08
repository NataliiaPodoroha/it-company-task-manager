from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(
            name="Developer"
        )
        self.worker = get_user_model().objects.create_user(
            username="john_smith",
            phone_number="+380955084755",
            first_name="John",
            last_name="Smith",
            password="Johns12345",
            position=self.position
        )

    def test_worker_phone_number_listed(self):
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.worker.phone_number)

    def test_worker_detailed_phone_number_listed(self):
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)

        self.assertContains(res, self.worker.phone_number)

    def test_additional_info_fields_in_worker_add(self):
        url = reverse("admin:task_manager_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "phone_number")
        self.assertContains(response, "Additional info")
