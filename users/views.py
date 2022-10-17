from django.shortcuts import render,redirect
from blog.forms import *
from users.forms import *
from django.urls import reverse_lazy
from users.models import *
from django.contrib.auth.decorators import login_required

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)

    form = ForgotPasswordForm()
    return render(request,'registration/forgot_password.html',{'form':form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/?signed=true')
        else:
            return render(request,'registration/register.html',{'form': form})


    form = RegisterForm()
    return render(request,'registration/register.html',{'form': form})
