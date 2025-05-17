from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "task"
        verbose_name_plural = "tasks"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "Urgent", "Urgent"
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        choices=Priority.choices,
        max_length=10,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="type_tasks"
    )
    assignees = models.ManyToManyField(
        "Worker",
        related_name="assigned_tasks"
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="project_tasks"
    )

    def __str__(self) -> str:
        return (f"{self.task_type.name if self.task_type else 'No type!'}: "
                f"{self.name}, {self.deadline}, {self.is_completed}, "
                f"{self.priority}")

    class Meta:
        ordering = ["deadline"]
        verbose_name = "task"
        verbose_name_plural = "tasks"


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.SET_NULL,
        null=True,
        related_name="position_workers",
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["id"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "position"
        verbose_name_plural = "positions"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "team"
        verbose_name_plural = "teams"


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-end_date"]
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self) -> str:
        return self.name
