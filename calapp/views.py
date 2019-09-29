from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Event
from .models import Task
from .models import Subtask
from .models import Category


# Create your views here.
def index(request):
    if (not request.user.is_authenticated):
        return HttpResponse("Not logged in!")
        
    all_events = Event.objects.filter(user__exact=request.user).order_by("event_name")
    tasks = Task.objects.filter(user__exact=request.user).order_by("deadline")
    subtasks = Subtask.objects.filter(user__exact=request.user).all
    categories = Category.objects.filter(user__exact=request.user).all
    
    template = loader.get_template("calapp/index.html")
    context = {
        "all_events": all_events,
        "tasks": tasks,
        "subtasks": subtasks,
        "categories": categories,
    }
    return HttpResponse(template.render(context, request))