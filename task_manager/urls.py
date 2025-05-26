from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    index,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    TaskTypeDetailView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDetailView,
    TaskDeleteView,
    WorkerListView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDetailView,
    WorkerDeleteView,
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDetailView,
    ProjectDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    PositionDetailView,
    TeamListView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    TeamDetailView, RegisterView,
)


urlpatterns = [
    path("", index, name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(next_page='register'), name='logout'),

    path("task-type/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task-type/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task-type/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task-type/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "task-type/<int:pk>/detail/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail"
    ),
    path("task/", TaskListView.as_view(), name="task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "task/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),

    path(
        "task/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "worker/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "worker/<int:pk>/detail/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),

    path(
        "worker/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path("project/", ProjectListView.as_view(), name="project-list"),
    path(
        "project/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "project/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "project/<int:pk>/detail/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path(
        "project/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
    path("position/", PositionListView.as_view(), name="position-list"),
    path(
        "position/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "position/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "position/<int:pk>/detail/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "position/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path("team/", TeamListView.as_view(), name="team-list"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path(
        "team/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="team-update"
    ),
    path(
        "team/<int:pk>/detail/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(
        "team/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete"
    ),

]
app_name = "task_manager"
