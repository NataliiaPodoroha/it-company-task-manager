from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import Position, Task, TaskType, Worker


class WorkerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        position = Position.objects.create(
            name="Developer"
        )
        get_user_model().objects.create_user(
            username="john_smith",
            phone_number="+380955084755",
            first_name="John",
            last_name="Smith",
            password="Johns12345",
            position=position
        )

    def test_worker_str(self):
        worker = Worker.objects.get(username="john_smith")

        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.first_name} {worker.last_name})"
        )

    def test_get_absolute_url(self):
        worker = Worker.objects.get(username="john_smith")
        self.assertEqual(worker.get_absolute_url(), f"/workers/{worker.id}/")


class TskModelTests(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        task_type = TaskType.objects.create(
            name="New feature"
        )
        Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2023-08-25",
            is_completed=False,
            priority="Medium",
            task_type=task_type,
        )

    def test_task_str(self):
        task = Task.objects.get(name="Test Task")

        self.assertEqual(
            str(task),
            f"{task.name} (Priority: {task.priority})"
        )

    def test_get_absolute_url(self):
        task = Task.objects.get(name="Test Task")
        self.assertEqual(task.get_absolute_url(), f"/tasks/{task.id}/")
