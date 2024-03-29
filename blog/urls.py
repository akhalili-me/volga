from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
     path('', views.Home,name='home'),

     # Post urls
     path('postarchive', views.PostListView.as_view(),name='archive'),
     path('post/<int:pk>', views.PostDetailView.as_view(),name='post'),
     path('post/create', views.PostCreateView.as_view(),name='post_create'),
     path('post/update/<int:pk>', views.PostUpdateView.as_view(),name='post_update'),
     path('post/delete/<int:pk>', views.PostDeleteView.as_view(),name='post_delete'),
     path('post/publish/<int:pk>', views.publish_post,name='post_publish'),

     #Comments
     path('post/ajax/addcomment/<int:pk>', views.add_comment,name='add_comment'),
     path('post/aprrove-comment/<int:pk>', views.approve_comment,name='approve_comment'),
     path('post/remove-comment/<int:pk>', views.remove_comment,name='remove_comment'),

     # Category Urls
     path('categories', views.CategoryListView.as_view(),name='category_list'),
     path('categories/<int:pk>', views.category_posts,name='category_posts'),
]