from django.shortcuts import render, redirect
from django.views.generic import View
from taskapp.models import Tasks, User
from taskapp.forms import RegistrationForms, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
        # usre = request.POST.get('username')
        usr = request.user
        # print(type(usre), type(usr))
        # usr_obj = User.objects.get(username=usr)
        task = request.POST.get('task')
        Tasks.objects.create(user=usr, task_name=task)
        messages.success(request, 'task has been created')
        return render(request, 'tasklist.html')
    
class TaskListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
        # qs = Tasks.objects.all()
            qs = request.user.tasks_set.all()
            return render(request, "tasklist.html", {'todos':qs})
        else:
            return redirect('signin')
class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Tasks.objects.get(id=id)
        return render(request, "task-detail.html", {'todo':qs})
    
class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Tasks.objects.filter(id=id).delete()
        messages.success(request, 'task deleted')

        return redirect('tasks')
    
class RegistrationFormView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForms()
        print('in am in get ')
        return render(request, 'registration-form.html', {'form':form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print('in am in post')
        form = RegistrationForms(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            form.save()
            messages.success(request, 'Registration completed')
            return redirect('tasks')
        else:
            print('im')
            messages.success(request, 'Registration Failed')
            return render(request, 'registration-form.html', {'form':form})
        
class LoginFormView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login-form.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        # print(form)
        # print(dir(form))
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            usr = authenticate(request, username=uname, password=pwd)
            print(usr)
        if usr:
            login(request, usr)
            return redirect('tasks')
        else:
            print('invalid cred')
            messages.success(request, 'Invalid credentials')
            return render(request, 'login.html', {'form':form})
        
def signout_view(request, *args, **kwargs):
    logout(request)
    return redirect('signin')