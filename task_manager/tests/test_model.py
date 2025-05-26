from datetime import datetime

from django.test import TestCase

from task_manager.models import TaskType, Task, Worker, Position, Team, Project


class ModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.project = Project.objects.create(
            name="Test Project",
            end_date="2025-11-11",
            team=self.team
        )
        self.position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create_user(
            username="Test username",
            password="test1213",
            first_name="Test First",
            last_name="Test Last"
        )
        self.task_type = TaskType.objects.create(name="Task Type")
        self.task = Task.objects.create(
            name="Test",
            description="Test Description",
            deadline=datetime.now(),
            priority="Urgent",
            task_type=self.task_type,
            project=self.project,
        )
        self.task.assignees.set([self.worker])

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Task Type")

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.task_type.name}: "
            f"{self.task.name}, {self.task.deadline}, "
            f"{self.task.is_completed}, {self.task.priority}")

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.username} "
            f"({self.worker.first_name} {self.worker.last_name})"
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), "Test Position")

    def test_team_str(self):
        self.assertEqual(str(self.team), "Test Team")

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")
