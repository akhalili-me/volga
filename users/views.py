from django.shortcuts import render,redirect
from blog.forms import *
from users.forms import *
from users.models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from blog.models import *

@user_passes_test(lambda u: u.is_authenticated==False,redirect_field_name='/')
def forgot_password(request):

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)

    form = ForgotPasswordForm()
    return render(request,'registration/forgot_password.html',{'form':form})


@user_passes_test(lambda u: u.is_authenticated==False,redirect_field_name='/')
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
 

@login_required
def user_profile(request):
    return render(request,'user_profile/profile.html')

@login_required
def user_posts(request):
    user = request.user
    user_posts = Post.objects.filter(author = user,published_Date__isnull=False).order_by('-published_Date')
    return render(request,'user_profile/user_posts.html',{'posts':user_posts})