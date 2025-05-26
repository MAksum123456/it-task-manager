from django.test import TestCase
from django.contrib.auth.models import Group
from task_manager.forms import WorkerCreationForm
from task_manager.models import Team, Position, Worker


class WorkerCreationFormTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.position = Position.objects.create(name="Test Position")
        self.group = Group.objects.create(name="Employee")

    def test_worker_creation_form_creates_user_and_assigns_group(self):
        form_data = {
            "username": "testuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
            "first_name": "Test",
            "last_name": "User",
            "position": self.position.id,
            "team": self.team.id,
        }

        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        worker = form.save()

        self.assertIsInstance(worker, Worker)
        self.assertEqual(worker.username, "testuser")
        self.assertEqual(worker.first_name, "Test")
        self.assertEqual(worker.last_name, "User")
        self.assertEqual(worker.position, self.position)
        self.assertEqual(worker.team, self.team)

        self.assertTrue(worker.groups.filter(name="Employee").exists())
