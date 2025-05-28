from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.urls import reverse

from task_manager.forms import (
    TaskTypeSearchForm,
    TaskSearchForm,
    WorkerSearchForm,
    PositionSearchForm,
    ProjectSearchForm,
    TeamSearchForm
)

from task_manager.models import Worker, TaskType, Task, Project, Position, Team
from task_manager.views import WorkerDeleteView, WorkerUpdateView


class ViewLoginRequiredTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Test Position")
        cls.team = Team.objects.create(name="Test Team")

        cls.worker = Worker.objects.create_user(
            username="user",
            password="pass",
            position=cls.position,
            team=cls.team
        )

        cls.project = Project.objects.create(
            name="Test Project",
            end_date="2025-12-25",
            team=cls.team
        )

        cls.task_type = TaskType.objects.create(name="ExampleType")

        cls.task = Task.objects.create(
            name="Test Task",
            description="Test",
            deadline="2030-01-01",
            priority="Urgent",
            task_type=cls.task_type,
            project=cls.project,
        )
        cls.task.assignees.add(cls.worker)

    def test_views_require_login(self):
        urls = [
            reverse("task_manager:task-type-list"),
            reverse("task_manager:task-type-create"),
            reverse("task_manager:task-type-update", args=[self.task_type.pk]),
            reverse("task_manager:task-type-delete", args=[self.task_type.pk]),
            reverse("task_manager:task-type-detail", args=[self.task_type.pk]),

            reverse("task_manager:task-list"),
            reverse("task_manager:task-create"),
            reverse("task_manager:task-update", args=[self.task.pk]),
            reverse("task_manager:task-delete", args=[self.task.pk]),
            reverse("task_manager:task-detail", args=[self.task.pk]),

            reverse("task_manager:worker-list"),
            reverse("task_manager:worker-create"),
            reverse("task_manager:worker-update", args=[self.worker.pk]),
            reverse("task_manager:worker-delete", args=[self.worker.pk]),
            reverse("task_manager:worker-detail", args=[self.worker.pk]),

            reverse("task_manager:position-list"),
            reverse("task_manager:position-create"),
            reverse("task_manager:position-update", args=[self.position.pk]),
            reverse("task_manager:position-delete", args=[self.position.pk]),
            reverse("task_manager:position-detail", args=[self.position.pk]),

            reverse("task_manager:team-list"),
            reverse("task_manager:team-create"),
            reverse("task_manager:team-update", args=[self.team.pk]),
            reverse("task_manager:team-delete", args=[self.team.pk]),
            reverse("task_manager:team-detail", args=[self.team.pk]),

            reverse("task_manager:project-list"),
            reverse("task_manager:project-create"),
            reverse("task_manager:project-update", args=[self.project.pk]),
            reverse("task_manager:project-delete", args=[self.project.pk]),
            reverse("task_manager:project-detail", args=[self.project.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f'/accounts/login/?next={url}')


class ViewPermissionRequiredTests(TestCase):
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

        self.group_admin = Group.objects.create(name="Administrator")
        self.group_employee = Group.objects.create(name="Employee")
        self.group_hr = Group.objects.create(name="HR")
        self.group_pm = Group.objects.create(name="Project Manager")
        self.group_tl = Group.objects.create(name="Team Leader")

        GROUP_PERMISSIONS = {
            "Administrator": [
                "add_task",
                "change_task",
                "delete_task",
                "view_task",
                "add_project",
                "change_project",
                "delete_project",
                "view_project",
                "add_worker",
                "change_worker",
                "delete_worker",
                "view_worker",
                "add_position",
                "change_position",
                "delete_position",
                "view_position",
                "add_team",
                "change_team",
                "delete_team",
                "view_team",
                "add_tasktype",
                "change_tasktype",
                "delete_tasktype",
                "view_tasktype",
            ],
            "Employee": [
                "view_task",
                "view_project",
                "view_worker",
                "view_position",
                "view_team",
                "view_tasktype"
            ],
            "HR": [
                "add_position",
                "change_position",
                "view_position",
                "add_worker",
                "change_worker",
                "view_worker"
            ],
            "Project Manager": [
                "add_project",
                "change_project",
                "delete_project",
                "view_position",
                "add_task",
                "change_task",
                "delete_task",
                "view_worker"
            ],
            "Team Leader": [
                "change_task",
                "view_project",
                "view_task",
                "view_team"
            ],

        }

        for group_name, perms in GROUP_PERMISSIONS.items():
            group = Group.objects.get(name=group_name)
            for codename in perms:
                try:
                    permission = Permission.objects.get(codename=codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Permission '{codename}' does not exist.")

        self.admin_user = Worker.objects.create_user(
            username="admin",
            password="1234",
            position=self.position,
            team=self.team
        )
        self.admin_user.groups.add(self.group_admin)

        self.employee_user = Worker.objects.create_user(
            username="employee",
            password="1234",
            position=self.position,
            team=self.team
        )
        self.employee_user.groups.add(self.group_employee)

        self.hr_user = Worker.objects.create_user(
            username="hr",
            password="1234",
            position=self.position,
            team=self.team
        )
        self.hr_user.groups.add(self.group_hr)

        self.project_manager_user = Worker.objects.create_user(
            username="project_manager",
            password="1234",
            position=self.position,
            team=self.team
        )
        self.project_manager_user.groups.add(self.group_pm)

        self.team_leader_user = Worker.objects.create_user(
            username="team_leader",
            password="1234",
            position=self.position,
            team=self.team
        )
        self.team_leader_user.groups.add(self.group_tl)

    def test_permission_required(self):
        ACCESS_MATRIX = {
            "task_manager:task-list": (
                [],
                ["Administrator", "Employee", "Team Leader"]
            ),
            "task_manager:task-create": (
                [],
                ["Administrator", "Project Manager"]
            ),
            "task_manager:task-update": (
                ["task"], ["Administrator", "Project Manager", "Team Leader"]
            ),
            "task_manager:task-delete": (
                ["task"],
                ["Administrator", "Project Manager"]
            ),
            "task_manager:task-detail": (
                ["task"], ["Administrator", "Employee", "Team Leader"]
            ),

            "task_manager:task-type-list": ([], ["Administrator", "Employee"]),
            "task_manager:task-type-create": ([], ["Administrator"]),
            "task_manager:task-type-update": (
                ["task_type"],
                ["Administrator"]
            ),
            "task_manager:task-type-delete": (
                ["task_type"],
                ["Administrator"]
            ),
            "task_manager:task-type-detail": (
                ["task_type"],
                ["Administrator", "Employee"]
            ),

            "task_manager:worker-list": (
                [], ["Administrator", "Employee", "Project Manager", "HR"]
            ),
            "task_manager:worker-create": ([], ["Administrator", "HR"]),
            "task_manager:worker-update": (
                ["worker"],
                ["Administrator", "HR"]
            ),
            "task_manager:worker-delete": (["worker"], ["Administrator"]),
            "task_manager:worker-detail": (
                ["worker"],
                ["Administrator", "Employee", "Project Manager", "HR"]
            ),
            "task_manager:project-list": (
                [],
                ["Administrator", "Employee", "Team Leader"]
            ),
            "task_manager:project-create": (
                [],
                ["Administrator", "Project Manager"]
            ),
            "task_manager:project-update": (
                ["project"],
                ["Administrator", "Project Manager"]
            ),
            "task_manager:project-delete": (
                ["project"],
                ["Administrator", "Project Manager"]
            ),
            "task_manager:project-detail": (
                ["project"],
                ["Administrator", "Employee", "Team Leader"]
            ),
            "task_manager:team-list": (
                [],
                ["Administrator", "Employee", "Team Leader"]
            ),
            "task_manager:team-create": ([], ["Administrator"]),
            "task_manager:team-update": (["team"], ["Administrator"]),
            "task_manager:team-delete": (["team"], ["Administrator"]),
            "task_manager:team-detail": (
                ["team"],
                ["Administrator", "Employee", "Team Leader"]
            ),

        }
        users = {
            "admin": self.admin_user,
            "employee": self.employee_user,
            "hr": self.hr_user,
            "project_manager": self.project_manager_user,
            "team_leader": self.team_leader_user,
        }

        objects = {
            "task": self.task.pk,
            "task_type": self.task_type.pk,
            "worker": self.worker.pk,
            "position": self.position.pk,
            "team": self.team.pk,
            "project": self.project.pk,
        }

        for username, user in users.items():
            self.client.login(username=username, password="1234")
            user_groups = [group.name for group in user.groups.all()]

            for viewname, (url_args_keys, allowed_groups) \
                    in ACCESS_MATRIX.items():
                args = [objects[key] for key in url_args_keys]
                url = reverse(viewname, args=args)

                expected_status = 200 if any(
                    g in allowed_groups for g in user_groups
                )else 403

                with self.subTest(user=username, view=viewname):
                    response = self.client.get(url)
                    self.assertEqual(
                        response.status_code,
                        expected_status,
                        msg=(
                            f"{username} (groups: {user_groups}) "
                            f"accessing {viewname} "
                            f"expected {expected_status}, "
                            f"got {response.status_code}"
                        )
                    )


class GetContextDateTest(TestCase):
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
        self.client.login(username="Test username", password="test1213")
        permission1 = Permission.objects.get(codename="view_tasktype")
        permission2 = Permission.objects.get(codename="view_task")
        permission3 = Permission.objects.get(codename="view_worker")
        permission4 = Permission.objects.get(codename="view_position")
        permission5 = Permission.objects.get(codename="view_project")
        permission6 = Permission.objects.get(codename="view_team")

        self.worker.user_permissions.add(
            permission1,
            permission2,
            permission3,
            permission4,
            permission5,
            permission6
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

    def test_task_type_context_date(self):
        response = self.client.get(reverse("task_manager:task-type-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], TaskTypeSearchForm
        )
        self.assertEqual(response.context["search_form"].initial["name"], "")

    def test_task_context_date(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], TaskSearchForm
        )
        self.assertEqual(response.context["search_form"].initial["name"], "")

    def test_worker_context_date(self):
        response = self.client.get(reverse("task_manager:worker-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], WorkerSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            ""
        )

    def test_position_context_date(self):
        response = self.client.get(reverse("task_manager:position-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], PositionSearchForm
        )
        self.assertEqual(response.context["search_form"].initial["name"], "")

    def test_project_context_date(self):
        response = self.client.get(reverse("task_manager:project-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ProjectSearchForm
        )
        self.assertEqual(response.context["search_form"].initial["name"], "")

    def test_team_context_date(self):
        response = self.client.get(reverse("task_manager:team-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], TeamSearchForm
        )
        self.assertEqual(response.context["search_form"].initial["name"], "")


class ViewQuerySetTest(TestCase):
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
        self.client.login(username="Test username", password="test1213")
        permission1 = Permission.objects.get(codename="view_tasktype")
        permission2 = Permission.objects.get(codename="view_task")
        permission3 = Permission.objects.get(codename="view_worker")
        permission4 = Permission.objects.get(codename="view_position")
        permission5 = Permission.objects.get(codename="view_project")
        permission6 = Permission.objects.get(codename="view_team")

        self.worker.user_permissions.add(
            permission1,
            permission2,
            permission3,
            permission4,
            permission5,
            permission6
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

    def test_task_type_view_queryset_filtered_by_query(self):
        TaskType.objects.create(name="Task Type1")
        TaskType.objects.create(name="Task Type2")

        response = self.client.get(
            reverse("task_manager:task-type-list") + "?name=type2"
        )
        self.assertEqual(response.status_code, 200)
        tasks_types = response.context["tasktype_list"]
        self.assertEqual(len(tasks_types), 1)
        self.assertEqual(tasks_types[0].name, "Task Type2")

    def test_task_view_queryset_filtered_by_query(self):
        Task.objects.create(
            name="Task1",
            description="Test Description",
            deadline=datetime.now(),
            priority="Urgent",
            task_type=self.task_type,
            project=self.project,
        )
        Task.objects.create(
            name="Task2",
            description="Test Description",
            deadline=datetime.now(),
            priority="Urgent",
            task_type=self.task_type,
            project=self.project,
        )

        response = self.client.get(
            reverse("task_manager:task-list") + "?name=task2"
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context["task_list"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, "Task2")

    def test_worker_view_queryset_filtered_by_query(self):
        Worker.objects.create_user(
            username="Test user1",
            password="<PASSWORD>",
            position=self.position,
            team=self.team
        )
        Worker.objects.create_user(
            username="Test User2",
            password="<PASSWORD>",
            position=self.position,
            team=self.team
        )

        response = self.client.get(
            reverse("task_manager:worker-list") + "?username=1"
        )
        self.assertEqual(response.status_code, 200)
        workers = response.context["worker_list"]
        self.assertEqual(len(workers), 1)
        self.assertEqual(workers[0].username, "Test user1")

    def test_position_view_queryset_filtered_by_query(self):
        Position.objects.create(name="Test Position1")
        Position.objects.create(name="Test Position2")

        response = self.client.get(
            reverse("task_manager:position-list") + "?name=position1"
        )
        self.assertEqual(response.status_code, 200)
        positions = response.context["position_list"]
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0].name, "Test Position1")

    def test_team_view_queryset_filtered_by_query(self):
        Team.objects.create(name="Test Team1")
        Team.objects.create(name="Test Team2 5")

        response = self.client.get(
            reverse("task_manager:team-list") + "?name=5"
        )
        self.assertEqual(response.status_code, 200)
        teams = response.context["team_list"]
        self.assertEqual(len(teams), 1)
        self.assertEqual(teams[0].name, "Test Team2 5")

    def test_project_view_queryset_filtered_by_query(self):
        Project.objects.create(
            name="Project 1",
            end_date="2025-11-11",
            team=self.team,
        )
        Project.objects.create(
            name="Project 1 main",
            end_date="2025-11-11",
            team=self.team,
        )

        response = self.client.get(
            reverse("task_manager:project-list") + "?name=main"
        )
        self.assertEqual(response.status_code, 200)
        projects = response.context["project_list"]
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].name, "Project 1 main")


User = get_user_model()


class DispatchTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Worker.objects.create_user(
            username="user1",
            password="testpass",
            first_name="User",
            last_name="One"
        )
        self.other_user = Worker.objects.create_user(
            username="user2",
            password="testpass",
            first_name="User",
            last_name="Two"
        )

    def test_dispatch_allows_self_access(self):
        request = self.factory.post(
            reverse("task_manager:worker-delete", kwargs={"pk": self.user.pk})
        )
        request.user = self.user

        view = WorkerDeleteView.as_view()
        response = view(request, pk=self.user.pk)

        self.assertIn(response.status_code, [200, 302])

    def test_dispatch_denies_other_user_access(self):
        request = self.factory.post(
            reverse(
                "task_manager:worker-delete", kwargs={"pk": self.other_user.pk}
            )
        )
        request.user = self.user

        view = WorkerDeleteView.as_view()

        with self.assertRaises(PermissionDenied):
            view(request, pk=self.other_user.pk)

    def test_dispatch_allows_self_update(self):
        request = self.factory.get(
            reverse("task_manager:worker-update", kwargs={"pk": self.user.pk})
        )
        request.user = self.user

        view = WorkerUpdateView.as_view()
        response = view(request, pk=self.user.pk)

        self.assertEqual(response.status_code, 200)

    def test_dispatch_denies_other_user_update(self):
        request = self.factory.get(
            reverse("task_manager:worker-update", kwargs={"pk": self.user.pk})
        )
        request.user = self.other_user

        view = WorkerUpdateView()
        view.kwargs = {"pk": self.user.pk}
        view.request = request

        with self.assertRaises(PermissionDenied):
            view.dispatch(request, pk=self.user.pk)
