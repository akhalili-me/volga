from django.urls import path
from blog import views
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [
     path('post/id', views.PostListView.as_view(),name='home'),
     path('post/<int:id>', views.PostDetailView.as_view(),name='post'),
     path('post/create', views.PostCreateView.as_view(),name='post_create'),
]