from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Event
from .models import Task
from .models import Subtask
from .models import Category


# Create your views here.
def index(request):
    all_events = Event.objects.order_by("event_name")
    tasks = Task.objects.order_by("?")
    subtasks = Subtask.objects.order_by("?")
    categories = Category.objects.order_by("?")
    template = loader.get_template("calapp/index.html")
    context = {
        "all_events": all_events,
        "tasks": tasks,
        "subtasks": subtasks,
        "categories": categories,
    }
    return HttpResponse(template.render(context, request))