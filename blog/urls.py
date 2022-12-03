from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
     path('', views.Home,name='home'),
     path('postarchive', views.PostListView.as_view(),name='archive'),
     path('post/<int:pk>', views.PostDetailView.as_view(),name='post'),
     path('post/create', views.PostCreateView.as_view(),name='post_create'),
     path('post/update/<int:pk>', views.PostUpdateView.as_view(),name='post_update'),
     path('post/delete/<int:pk>', views.PostDeleteView.as_view(),name='post_delete'),
     path('post/drafts', views.DraftListView.as_view(),name='post_draft'),
     path('post/publish/<int:pk>', views.publish_post,name='post_publish'),
     path('post/comment/<int:pk>', views.add_comment,name='add_comment'),
     path('post/aprrove-comment/<int:pk>', views.approve_comment,name='approve_comment'),
     path('post/remove-comment/<int:pk>', views.remove_comment,name='remove_comment'),
     path('categories', views.CategoryListView.as_view(),name='category_list'),
]