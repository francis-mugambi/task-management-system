from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='index'),    
    path('login/', views.login, name='login'),
    path('create-account/', views.createAccount, name='create-account'),
    path('profile/', views.profile, name='profile'),
    path('tasks/', views.tasks, name='tasks'),
    path('add-task/', views.addTask, name='add-task'),
    path('update-task/<str:str>', views.updateTask, name='update-task'),
    path('view-task/<str:str>', views.viewTask, name='view-task'),
    path('delete-task/<str:str>', views.deleteTask, name='delete-task'),
    
]