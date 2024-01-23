from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, UpdateView
from taskapp.models import Tasks, User
from taskapp.forms import RegistrationForms, LoginForm, TaskUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

# Create your views here.

def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error('please sign in')
            return redirect('signin')
        else:
            return fn(request, *args, **kwargs)
    return wrapper

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration.html")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")
    
@method_decorator(signin_required, name='dispatch')
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
        qs = request.user.tasks_set.all()
        return render(request, "tasklist.html", {'todos':qs})
    
        # return render(request, 'tasklist.html')
    

'''using the normal List View'''
# method_decorator(signin_required, name='dispatch')
# class TaskListView(View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#         # qs = Tasks.objects.all()
#             qs = request.user.tasks_set.all()
#             return render(request, "tasklist.html", {'todos':qs})
#         else:
#             return redirect('signin')

        
'''using the List View'''
method_decorator(signin_required, name='dispatch')
class TaskListView(ListView):
    model = Tasks
    template_name = 'tasklist.html'
    context_object_name = 'todos'
    def get_queryset(self):
        return Tasks.objects.filter(user=self.request.user)
    #inbuilt it will be below like:
    #{'object_list':qs}
    #to override this we used the above statement

'''using the normal Detail View'''
# @method_decorator(signin_required, name='dispatch')
# class TaskDetailView(View):
#     def get(self, request, *args, **kwargs):
#         id = kwargs.get('id')
#         qs = Tasks.objects.get(id=id)
#         return render(request, "task-detail.html", {'todo':qs})


'''using the DetailView'''
@method_decorator(signin_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Tasks
    template_name = "task-detail.html"
    context_object_name = 'todo'
    pk_url_kwarg = 'id'


'''using the normal update view'''
# class TaskUpdateView(View):

#     def get(self, request, *args, **kwargs):
#         id = kwargs.get('id')
#         qs = Tasks.objects.get(id=id)
#         forms = TaskUpdateForm(instance=qs)
#         return render(request, 'task-update.html',{'forms':forms})


'''using the update view'''
class TaskUpdateView(UpdateView):
    model = Tasks
    form_class = TaskUpdateForm
    # print(form_class.)
    template_name = "task-update.html"
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('tasks')


@method_decorator(signin_required, name='dispatch')
class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Tasks.objects.filter(id=id).delete()
        messages.success(request, 'task deleted')
        return redirect('tasks')


# @method_decorator(signin_required, name='dispatch') 
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
            return redirect('signin')
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
        
@signin_required
def signout_view(request, *args, **kwargs):
    logout(request)
    return redirect('signin')