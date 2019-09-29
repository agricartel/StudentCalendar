from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
    
    

from .forms import TaskForm
from .forms import ModelTaskForm
def new_task(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ModelTaskForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            newTask = Task(
                user=request.user,
                task_name=form.cleaned_data['task_name'],
                deadline=form.cleaned_data['deadline'],
                priority=form.cleaned_data['priority'],
                category=form.cleaned_data['category'],
                completed=False,
                estimatedDuration=form.cleaned_data['estimatedDuration'],
            )
            newTask.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/cal/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ModelTaskForm()

    return render(request, 'calapp/newtask.html', {'form': form})
    

def delete_task(request):
    task_id_to_delete = request.GET.get("id", default="BADID")
    if task_id_to_delete != "BADID":
        Task.objects.filter(id__exact=task_id_to_delete).delete()
    return HttpResponseRedirect('/cal/')
    
def delete_event(request):
    event_id_to_delete = request.GET.get("id", default="BADID")
    if event_id_to_delete != "BADID":
        Event.objects.filter(id__exact=event_id_to_delete).delete()
    return HttpResponseRedirect('/cal/')
    
from . import allocateTime
def allocate_time_for_task(request):
    task_id_to_alloc = request.GET.get("id", default="BADID")
    if task_id_to_alloc == "BADID":
        return HttpResponseRedirect('/cal/')
    got_task = Task.objects.get(id__exact=task_id_to_alloc)