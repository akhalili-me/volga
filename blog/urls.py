from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
     path('', views.PostListView.as_view(),name='home'),
     path('post/<int:pk>', views.PostDetailView.as_view(),name='post'),
     path('post/create', views.PostCreateView.as_view(),name='post_create'),
     path('post/update/<int:pk>', views.PostUpdateView.as_view(),name='post_update'),
     path('post/delete/<int:pk>', views.PostDeleteView.as_view(),name='post_delete'),
     path('post/drafts', views.DraftListView.as_view(),name='post_draft'),
     path('post/comment/<int:pk>', views.add_comment,name='add_comment'),
     path('post/aprrovecomment/<int:pk>', views.approve_comment,name='approve_comment'),

]