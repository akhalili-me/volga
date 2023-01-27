from django.shortcuts import render,redirect
from blog.forms import *
from users.forms import *
from users.models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from blog.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DeleteView
from blog.mixins import * 
from django.urls import reverse_lazy


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

class UserPostsListView(LoginRequiredMixin,ListView):
    model = Post
    login_url = '/login/'
    template_name = 'user_profile/user_posts.html'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user,published_Date__isnull=False).order_by('-published_Date')


class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    login_url = '/login/'
    template_name = 'user_profile/post_drafts.html'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user,published_Date__isnull=True).order_by('-created_Date')

class CommentListView(LoginRequiredMixin,ListView):
    model = Comment
    login_url = '/login/'
    template_name = 'user_profile/user_comments.html'
    paginate_by = 4

    def get_queryset(self):
        return Comment.objects.filter(author = self.request.user,approved_Comment=True).order_by('-created_Date')


class CommentDeleteView(AuthorCheckMixin,DeleteView):
    model = Comment
    login_url = '/login'
    template_name = 'user_profile/comment_delete.html'
    success_url = reverse_lazy('users:user_comments')




