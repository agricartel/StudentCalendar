from django import forms

from .models import Event
from .models import Task
from .models import Subtask
from .models import Category


class TaskForm(forms.Form):
    task_name = forms.CharField(label="Task Name", max_length=300)
    task_deadline = forms.DateTimeField(label="Deadline")
    task_priority = forms.ChoiceField(label="Priority", choices=Task.PRIORITY_CHOICES)
    task_category = forms.ModelChoiceField(queryset=Category.objects.filter(user__exact=request.user).all, empty_label="(No Category)")
    task_duration = forms.DurationField(label="Estimated Duration")