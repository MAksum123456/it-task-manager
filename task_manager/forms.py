from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import Worker


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "team",
            "first_name",
            "last_name",
        )

    """ When creating a user, an employee group is provided"""
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = Group.objects.get(name="Employee")
            user.groups.add(group)
        return user


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-dark",
            "style": "width: 200px; color: white;",
            "placeholder": "Search by name"
        }),
    )


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-dark",
            "style": "width: 200px; color: white;",
            "placeholder": "Search by name"
        }),
    )


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-dark",
            "style": "width: 200px; color: white;",
            "placeholder": "Search by name"
        }),
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-dark",
            "style": "width: 200px; color: white;",
            "placeholder": "Search by username"
        }),
    )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-dark",
            "style": "width: 200px; color: white;",
            "placeholder": "Search by name"
        }),
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-light border-dark",
            "style": "width: 200px; color: white;",
            "placeholder": "Search by name"
        })
    )
