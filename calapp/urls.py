from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('caltest/', views.indextest, name='indextest'),
    path('newtask/', views.new_task, name='newtask'),
    path('deletetask/', views.delete_task, name='deletetask'),
    path('deleteevent/', views.delete_event, name='deleteevent'),
]