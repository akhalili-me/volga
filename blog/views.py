from django.shortcuts import render,get_object_or_404,redirect
from blog.models import *
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404
from blog.mixins import * 
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F, Sum

def Home(request):
    trending_articles = Post.objects.filter(published_Date__isnull=False).order_by('-views')[:4].only('title','header_image','like','published_Date')
    latest_articles = Post.objects.filter(published_Date__isnull=False).order_by('-published_Date')[:6].only('title','header_image','like','published_Date','summary')
    categories = Category.objects.all()
    main_3_articles = Post.objects.filter(published_Date__isnull=False).annotate(total_popularity=Sum(F('like') + F('views'))).order_by('-total_popularity')[:3].select_related('category')
    most_liked_articles = Post.objects.filter(published_Date__isnull=False).order_by('-like')[:4]

    context = {
        'trending': trending_articles,
        'latest': latest_articles,
        'categories': categories,
        'latest_liked': most_liked_articles,
        'main_articles': main_3_articles
    }

    return render(request, 'main/home.html', context)



class PostListView(ListView):
    queryset = Post.objects.filter(published_Date__isnull=False).order_by('-published_Date')
    template_name = 'blog/post_archive.html'
    paginate_by = 4

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user

        # Check if the post is published or the user is the author
        if post.published_Date is None and post.author != user:
            raise Http404('Page not found')

        context['author_permission'] = (post.author == user)

        form = CommentForm()
        context['form'] = form

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:post', args=['<pk>'])
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        if form.cleaned_data['publish']:
            self.object.publish_post()
        
        return response


class PostUpdateView(AuthorCheckMixin,UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'blog/post_create.html'



class PostDeleteView(AuthorCheckMixin,DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:home')


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'blog/category_list.html'

#############################################
#############################################

def category_posts(request,pk):
    category = get_object_or_404(Category,id=pk)
    posts = Post.objects.filter(category=category)
    return render(request,'blog/category_posts.html',{'posts':posts,'category':category})


@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post,id=pk)

    if post.author != request.user or post.published_Date != None:
        raise Http404()

    if request.method == 'POST':
        post.publish_post()
        return redirect('blog:post',pk=pk)
    
    return render(request,'blog/post_publish.html',{'object':post})


@login_required
def add_comment(request,pk):
    # Get the post object or raise a 404 error if it does not exist
    post = get_object_or_404(Post,id=pk)

    if request.method == "POST":
        # Get the comment form and validate it
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.post = post
            form.instance.author = request.user
            comment = form.save()
            # Serialize the comment object and return it as a JSON response
            ser_instance = serializers.serialize('json', [ comment, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # Return the form errors as a JSON response
            return JsonResponse({"error": form.errors}, status=400)

    # Return an empty JSON response with an error status code
    return JsonResponse({"error": ""}, status=400)



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


        