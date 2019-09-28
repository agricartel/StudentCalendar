from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Category
admin.site.register(Category)

from .models import Task
admin.site.register(Task)

from .models import Subtask
admin.site.register(Subtask)

from .models import Event
admin.site.register(Event)