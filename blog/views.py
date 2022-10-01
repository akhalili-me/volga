from django.shortcuts import render
from blog.models import *
from django.views.generic import CreateView,TemplateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import *
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import Http404

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
    # redirect_field_name = '/'
    template_name = 'blog/post_create.html'

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm
    # redirect_field_name = '/'
    template_name = 'blog/post_create.html'


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    login_url = '/login'
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')

class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    login_url = '/login/'
    queryset = Post.objects.filter(Q(published_Date__isnull=True) | Q(published_Date = ''))\
        .order_by('-created_Date')
    template_name = 'blog/post_drafts.html'
    


#############################################
#############################################

@login_required
def add_comment(request,pk):

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if CommentForm.is_valid():

            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = Post.objects.get(id=pk)
            new_comment.save()
            
            pass

    
    form = CommentForm()
    render(request,'blog/add_comment.html',{'comment_form': form})





@login_required
def approve_comment(request,pk):

    if request.user.is_superuser:
        if request.method == 'POST':
            comment = Comment.objects.get(id=pk)
            comment.approve()
        else:
            not_approved_comments = Comment.objects.filter('approved_Comment' == False)
            render(request,'blog/approve_comments.html',{'comments': not_approved_comments})
    else:
        Http404('Page not found')