from django.db import models
from django.conf import settings

# Create your models here.
# class User(models.Model):
    # username = models.CharField(max_length=200)
    # pass_hash = models.CharField(max_length=128)
    # pass_salt = models.CharField(max_length=128)
    # email = models.EmailField()
    
class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category_name = models.CharField(max_length=300)
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE)
    color_hex = models.CharField(max_length=6)
   
class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    task_name = models.CharField(max_length=300)
    deadline = models.DateTimeField()
    PRIORITY_CHOICES = (
        ("HIGH_PRI", "High"),
        ("MED_PRI", "Medium"),
        ("LOW_PRI", "Low"),
    )
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default="MED_PRI")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    completed = models.BooleanField()
    
class Subtask(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    subtask_name = models.CharField(max_length=300)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField()
    
class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    event_name = models.CharField(max_length=300)
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.DurationField()