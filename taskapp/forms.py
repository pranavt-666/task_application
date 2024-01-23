from django import forms
from django.contrib.auth.models import User
from taskapp.models import Tasks


class RegistrationForms(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 
                  'username', 'email', 'password']
        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control', }),
            'password':forms.PasswordInput(attrs={'class':'form-control', "placeholder":"Enter password"}),
        }
        

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-info", "placeholder":"Enter username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info", "placeholder":"Enter password"}))

        
class TaskUpdateForm(forms.ModelForm):

    class Meta:
        model = Tasks
        fields = ['task_name', 'active']