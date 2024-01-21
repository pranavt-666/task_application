"""
URL configuration for task_application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from taskapp.views import IndexView, RegistrationView, LoginView, TaskListView, AddTaskView, TaskDetailView, TaskDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', IndexView.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('tasklist/', TaskListView.as_view(), name='tasks'),
    path('addtask/', AddTaskView.as_view(), name='add-task'),
    path('tasklist/<int:id>', TaskDetailView.as_view(), name='task-detail'),
    path('tasklist/<int:id>/remove', TaskDeleteView.as_view(), name='task-delete'),

]


