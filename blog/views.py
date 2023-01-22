from django.shortcuts import render,get_object_or_404,redirect
from blog.models import *
from django.views.generic import CreateView,TemplateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import Http404
from blog.mixins import * 
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers

def Home(request):

    trending_articles = Post.objects.filter(published_Date__isnull=False).order_by('-views')[:4]
    latest_articles = Post.objects.filter(published_Date__isnull=False).order_by('-published_Date')[:6]
    categories = Category.objects.all()
    most_liked_articles = Post.objects.filter(published_Date__isnull=False).order_by('-like')[:4]

    dup_post_list = list(most_liked_articles) + list(trending_articles) 
    post_list = [*set(dup_post_list)]
    
    main_3_articles = []
    for i in range(3):
        main_3_articles.append(post_list[i])
        del [post_list[i]]

    for i in range(len(post_list)):
        post_popularity = post_list[i].like + post_list[i].views

        for idx, main in enumerate(main_3_articles):
            main_popularity = main.like + main.views
            if post_popularity > main_popularity:
                main_3_articles[idx] = post_list[i]
                break

    context = {'trending':trending_articles,'latest': latest_articles,'categories':
                categories,'latest_liked':most_liked_articles,'main_articles': main_3_articles}

    return render(request,'main/home.html',context)

class PostListView(ListView):
    queryset = Post.objects.filter(published_Date__isnull=False).order_by('-published_Date')
    template_name = 'blog/post_archive.html'
    paginate_by = 4


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object ()

        form = CommentForm()
        context['form'] = form

        if post.published_Date is None and post.author != self.request.user:
            raise Http404('Page not found')

        if post.author == self.request.user:
            context['author_permission'] = True

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


class PostUpdateView(AuthorCheckMixin,UpdateView):
    login_url = '/login/'
    model = Post
    form_class = UpdateForm
    template_name = 'blog/post_create.html'



class PostDeleteView(AuthorCheckMixin,DeleteView):
    model = Post
    login_url = '/login'
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
    if request.method == 'POST':
        post = get_object_or_404(Post,id=pk)
        post.publish_post()
        return redirect('blog:post',pk=pk)


@login_required
def add_comment(request,pk):

    post = get_object_or_404(Post,id=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            ser_instance = serializers.serialize('json', [ comment, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
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


        