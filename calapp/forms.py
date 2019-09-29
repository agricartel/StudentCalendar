from django import forms

from django.forms import ModelForm

from .models import Event
from .models import Task
from .models import Subtask
from .models import Category


class TaskForm(forms.Form):

    user = None
        
    task_name = forms.CharField(label="Task Name", max_length=300)
    task_deadline = forms.DateTimeField(label="Deadline")
    task_priority = forms.ChoiceField(label="Priority", choices=Task.PRIORITY_CHOICES)
    task_category = None
    #task_category = forms.ModelChoiceField(queryset=Category.objects.filter(user__exact=request.user).all, empty_label="(No Category)")
    task_duration = forms.DurationField(label="Estimated Duration")
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.task_category = forms.ModelChoiceField(queryset=Category.objects.filter(user__exact=self.user).all(), empty_label="(No Category)")
        
        
class ModelTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["task_name", "deadline", "priority", "category", "estimatedDuration"]