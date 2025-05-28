from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    WorkerCreationForm,
    TaskTypeSearchForm,
    TaskSearchForm,
    TeamSearchForm,
    WorkerSearchForm,
    PositionSearchForm,
    ProjectSearchForm
)
from .models import (
    TaskType,
    Task,
    Worker,
    Project,
    Position,
    Team
)


def custom_permission_denied(request, exception=None):
    user = request.user
    if user.is_authenticated:
        permissions = user.get_all_permissions()
    else:
        permissions = []
    return render(
        request,
        "errors/403.html",
        {"permissions": permissions},
        status=403
    )


def index(request: HttpRequest) -> HttpResponse:
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_tasks": Task.objects.count(),
        "num_workers": Worker.objects.count(),
        "num_projects": Project.objects.count(),
        "num_visits": num_visits + 1,
        "username": request.user.username
        if request.user.is_authenticated else "Guest"
    }
    return render(request, "task_manager/index.html", context)


class TaskTypeListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = TaskType
    paginate_by = 15
    permission_required = "task_manager.view_tasktype"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.prefetch_related("type_tasks")
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskTypeCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    permission_required = "task_manager.add_tasktype"


class TaskTypeUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    permission_required = "task_manager.change_tasktype"


class TaskTypeDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = TaskType
    success_url = reverse_lazy("task_manager:task-type-list")
    permission_required = "task_manager.delete_tasktype"


class TaskTypeDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView
):
    model = TaskType
    queryset = TaskType.objects.all().prefetch_related("type_tasks")
    permission_required = "task_manager.view_tasktype"


class TaskListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = Task
    paginate_by = 15
    permission_required = "task_manager.view_task"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")
    permission_required = "task_manager.add_task"


class TaskUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")
    permission_required = "task_manager.change_task"


class TaskDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = Task
    success_url = reverse_lazy(LoginRequiredMixin, "task_manager:task-list")
    permission_required = "task_manager.delete_task"


class TaskDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView
):
    model = Task
    queryset = Task.objects.select_related(
        "project",
        "task_type"
    ).prefetch_related("assignees")
    permission_required = "task_manager.view_task"


class WorkerListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = Worker
    paginate_by = 15
    permission_required = "task_manager.view_worker"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username},
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.select_related("position", "team")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")

    permission_required = "task_manager.add_worker"


class WorkerUpdateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Worker
    permission_required = 'task_manager.change_worker'
    fields = ['username', 'first_name', 'last_name', 'position', 'team']
    success_url = reverse_lazy("task_manager:worker-list")

    def dispatch(self, request, *args, **kwargs):
        worker = self.get_object()
        if worker.pk != request.user.pk:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class WorkerDeleteView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Worker
    permission_required = 'task_manager.delete_worker'
    success_url = reverse_lazy("task_manager:worker-list")

    def dispatch(self, request, *args, **kwargs):
        worker = self.get_object()
        if worker.pk != request.user.pk:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)


class WorkerDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView
):
    model = Worker
    queryset = Worker.objects.select_related(
        "position",
        "team",
    ).prefetch_related("assigned_tasks")
    permission_required = "task_manager.view_worker"


class ProjectListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = Project
    paginate_by = 15
    permission_required = "task_manager.view_project"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class ProjectCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:project-list")
    permission_required = "task_manager.add_project"


class ProjectUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:project-list")
    permission_required = "task_manager.change_project"


class ProjectDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = Project
    success_url = reverse_lazy("task_manager:project-list")
    permission_required = "task_manager.delete_project"


class ProjectDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView
):
    model = Project
    queryset = Project.objects.select_related(
        "team"
    ).prefetch_related("project_tasks")
    permission_required = "task_manager.view_project"


class PositionListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = Position
    paginate_by = 15
    permission_required = "task_manager.view_position"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class PositionCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
    permission_required = "task_manager.add_position"


class PositionUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")
    permission_required = "task_manager.change_position"


class PositionDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")
    permission_required = "task_manager.delete_position"


class PositionDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView
):
    model = Position
    queryset = Position.objects.prefetch_related("position_workers")
    permission_required = "task_manager.view_position"


class TeamListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.ListView
):
    model = Team
    paginate_by = 15
    permission_required = "task_manager.view_team"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TeamSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Team.objects.prefetch_related(
            "team_projects",
            "team_workers"
        )
        form = TeamSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TeamCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.CreateView
):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team-list")
    permission_required = "task_manager.add_team"


class TeamUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.UpdateView
):
    model = Team
    fields = "__all__"
    success_url = reverse_lazy("task_manager:team-list")
    permission_required = "task_manager.change_team"


class TeamDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DeleteView
):
    model = Team
    success_url = reverse_lazy("task_manager:team-list")
    permission_required = "task_manager.delete_team"


class TeamDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    generic.DetailView
):
    model = Team
    queryset = Team.objects.prefetch_related("team_projects", "team_workers")
    permission_required = "task_manager.view_team"


class RegisterView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
