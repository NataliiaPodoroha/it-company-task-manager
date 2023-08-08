from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Task, TaskType, Worker


INDEX_LIST_URL = reverse("task_manager:index")
POSITION_LIST_URL = reverse("task_manager:position-list")
TASK_LIST_URL = reverse("task_manager:task-list")
TASK_TYPE_LIST_URL = reverse("task_manager:task-type-list")
WORKER_LIST_URL = reverse("task_manager:worker-list")


class PublicTests(TestCase):
    def test_index_login_required(self):
        response = self.client.get(INDEX_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_position_list_login_required(self):
        response = self.client.get(POSITION_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_task_list_login_required(self):
        response = self.client.get(TASK_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_task_type_list_login_required(self):
        response = self.client.get(TASK_TYPE_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="Architect"
        )
        self.task_type = TaskType.objects.create(
            name="New feature"
        )
        self.user = get_user_model().objects.create_user(
            username="john_smith",
            phone_number="+380955084755",
            first_name="John",
            last_name="Smith",
            password="Johns12345",
            position=self.position
        )

        self.client.force_login(self.user)

    def test_index(self):
        response = self.client.get(INDEX_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/index.html")

    def test_position_list(self):
        response = self.client.get(POSITION_LIST_URL)
        positions = Position.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions),
        )
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_task_list(self):
        Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2023-08-25",
            is_completed=False,
            priority="Medium",
            task_type=self.task_type,
        )
        response = self.client.get(TASK_LIST_URL)
        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks),
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_task_type_list(self):
        response = self.client.get(TASK_TYPE_LIST_URL)
        task_types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types),
        )
        self.assertTemplateUsed(response, "task_manager/task_type_list.html")

    def test_worker_list(self):
        response = self.client.get(WORKER_LIST_URL)
        workers = Worker.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers),
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_create_worker(self):

        form_data = {
            "username": "test_user",
            "password1": "Pass123test",
            "password2": "Pass123test",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+380955084759",
            "position": self.position.id,
        }
        self.client.post(reverse("task_manager:worker-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.phone_number, form_data["phone_number"])
