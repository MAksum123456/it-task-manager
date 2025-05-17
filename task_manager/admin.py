from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Task, TaskType, Worker, Project, Position, Team)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "end_date", "team")
    list_filter = ("end_date",)
    search_fields = ("name",)
    list_select_related = ("team",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "priority", "task_type", "project")
    list_filter = ("deadline", "priority", "is_completed")
    search_fields = ("name",)
    autocomplete_fields = ("task_type", "project", "assignees")



@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "team")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "team")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                        "team",
                    )
                },
            ),
        )
    )
    search_fields = ("username", "position__name", "team__name")
    list_filter = UserAdmin.list_filter + ("position", "team")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
