from django.shortcuts import render
from blog.models import *
from django.views.generic import CreateView,TemplateView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import *

# class Home(TemplateView):
#     template_name = 'main/home.html'


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-published_Date')
    template_name = 'main/home.html'


class PostDetailView(DetailView):
    model: Post
    template_name = 'blog/post.html'


class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

