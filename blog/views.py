from django.shortcuts import render,get_object_or_404,redirect
from blog.models import *
from django.views.generic import CreateView,TemplateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404

# class Home(TemplateView):
#     template_name = 'main/home.html'

def Home(request):
    trending_articles = Post.objects.filter(published_Date__isnull=False).order_by('-views')[:4]
    latest_articles = Post.objects.filter(published_Date__isnull=False).order_by('-published_Date')[:6]
    categories = Category.objects.all()
    latest_liked_articles = Post.objects.filter(published_Date=None).order_by('-like')[:3]

    return render(request,'main/home.html')

class PostListView(ListView):
    queryset = Post.objects.filter(published_Date__isnull=False).order_by('-published_Date')
    template_name = 'blog/post_archive.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Post.objects.get(pk = self.kwargs['pk'])

        if post.published_Date is None :
            raise Http404('Page not found')

        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login'
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        self.post = form.save(commit=False)
        self.post.author = self.request.user
        self.post.save()
        if form.cleaned_data['publish'] == True:
            self.post.publish_post()

        return redirect('/')


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
    queryset = Post.objects.filter(published_Date__isnull=True).order_by('-created_Date')
    template_name = 'blog/post_drafts.html'
    

class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'blog/category_list.html'

#############################################
#############################################

@login_required
def publish_post(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(Post,id=pk)
        post.publish_post()
        return redirect('blog:post',pk=pk)


@login_required
def add_comment(request,pk):
    post = get_object_or_404(Post,id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if CommentForm.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post',pk=post.id)
    else:
        form = CommentForm()
        render(request,'blog/add_comment.html',{'comment_form': form})



@login_required
def approve_comment(request,pk):
    if request.user.is_superuser:
        comment = get_object_or_404(Comment,id=pk)
        if request.method == 'POST':
            comment.approve()
            return ##To DO
        else:
            not_approved_comments = Comment.objects.filter('approved_Comment' == False)
            render(request,'blog/approve_comments.html',{'comments': not_approved_comments})
    else:
        raise Http404('Page not found')


@login_required
def remove_comment(request,pk):
    if request.user.is_superuser:
        comment = get_object_or_404(Comment,id=pk)
        comment.delete()
        return ##To DO
    else:
        raise Http404('Page not found')


        