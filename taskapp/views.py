from django.shortcuts import render, redirect
from django.views.generic import View
from taskapp.models import Tasks
# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration.html")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")
    

class AddTaskView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "taskadd.html")
    def post(self, request, *args, **kwargs):
        name = request.POST.get('username')
        task = request.POST.get('task')
        Tasks.objects.create(username=name, task_name=task)
        return render(request, 'taskadd.html')
    
class TaskListView(View):
    def get(self, request, *args, **kwargs):
        qs = Tasks.objects.all()
        return render(request, "tasklist.html", {'todos':qs})

class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Tasks.objects.get(id=id)
        return render(request, "task-detail.html", {'todo':qs})
    
class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Tasks.objects.filter(id=id).delete()
        return redirect('tasks')