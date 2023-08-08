from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import (
    PositionSearchForm,
    TaskSearchForm,
    TaskTypeSearchForm,
    WorkerCreationForm,
    WorkerSearchForm,
    WorkerUpdateForm
)

from task_manager.models import Position, Task, TaskType


class WorkerTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="Developer"
        )

        self.form_data = {
            "username": "test_user",
            "password1": "Pass123test",
            "password2": "Pass123test",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+380955084759",
            "position": self.position,
        }
        self.form = WorkerCreationForm(data=self.form_data)

    def test_worker_creation_is_valid(self):
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.cleaned_data, self.form_data)

    def test_phone_number_equal_13(self):
        phone_numbers = ["+3809550847511", "+3809550847"]

        for phone_number in phone_numbers:
            form_data = {"phone_number": phone_number}
            form = WorkerUpdateForm(data=form_data)

            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors["phone_number"][0],
                "Phone number should consist of 13 characters"
            )

    def test_phone_number_first_character(self):
        form_data = {"phone_number": "1380955084751"}

        form = WorkerUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["phone_number"][0],
            "Phone number should start with a character '+'"
        )

    def test_phone_number_last_5_characters_digits(self):
        form_data = {"phone_number": "+A80955084751"}

        form = WorkerUpdateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["phone_number"][0],
            "Last 12 characters should be digits"
        )


class TaskTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="Developer"
        )
        self.task_type = TaskType.objects.create(
            name="Bug"
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

    def test_create_task(self):
        response = self.client.post(
            reverse("task_manager:task-create"),
            {
                "name": "Test Task",
                "description": "Test description",
                "deadline": "2023-08-25",
                "is_completed": False,
                "priority": "Medium",
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Task.objects.get(id=self.user.tasks.first().id).name, "Test Task"
        )

    def test_update_task(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2023-08-25",
            is_completed=False,
            priority="Medium",
            task_type=self.task_type,
        )
        response = self.client.post(
            reverse("task_manager:task-update", kwargs={"pk": task.id}),
            {
                "pk": task.id,
                "description": "Test description",
                "deadline": "2023-08-25",
                "is_completed": False,
                "priority": "Medium",
                "name": "Not Test Task",
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
            },
        )
        Task.objects.get(id=task.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(id=task.id).name, "Not Test Task")

    def test_delete_task(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2023-08-25",
            is_completed=False,
            priority="Medium",
            task_type=self.task_type,
        )
        response = self.client.post(
            reverse("task_manager:task-delete", kwargs={"pk": task.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(
            name="Designer"
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

    def test_task_search_form(self):
        Task.objects.create(
            name="Test Task",
            description="Test description",
            deadline="2023-08-25",
            is_completed=False,
            priority="Medium",
            task_type=self.task_type,
        )
        form_data = {"name": "Test"}
        form = TaskSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = Task.objects.filter(name="Test Task")

        response = self.client.get(
            reverse("task_manager:task-list") + "?name=" + form_data["name"]
        )
        self.assertEqual(
            list(response.context["task_list"]), list(expected_result)
        )

    def test_position_search_form(self):
        form_data = {"name": "Designer"}
        form = PositionSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = Position.objects.filter(name="Designer")

        response = self.client.get(
            reverse(
                "task_manager:position-list") + "?name=" + form_data["name"]
        )
        self.assertEqual(
            list(response.context["position_list"]), list(expected_result)
        )

    def test_task_type_search_form(self):
        form_data = {"name": "New"}
        form = TaskTypeSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = TaskType.objects.filter(name="New feature")

        response = self.client.get(
            reverse(
                "task_manager:task-type-list"
            ) + "?name=" + form_data["name"]
        )
        self.assertEqual(
            list(response.context["task_type_list"]), list(expected_result)
        )

    def test_worker_search_form(self):
        form_data = {"username": "john"}
        form = WorkerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        expected_result = get_user_model().objects.filter(
            username="john_smith"
        )

        response = self.client.get(
            reverse(
                "task_manager:worker-list"
            ) + "?username=" + form_data["username"]
        )
        self.assertEqual(
            list(response.context["worker_list"]), list(expected_result)
        )
