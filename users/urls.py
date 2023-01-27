from django.urls import path
from django.contrib.auth import views
from users.views import *
from users.forms import *

app_name = 'users'

urlpatterns = [
     #Athentication
     path('login/', views.LoginView.as_view(authentication_form = UserLoginForm,redirect_authenticated_user=True),name='login'),
     path('logout', views.LogoutView.as_view(next_page = '/'),name='logout'),
     path('register',register,name='register'),

     #Profile
     path('profile',user_profile,name='profile'),
     path('profile/posts',UserPostsListView.as_view(),name='user_posts'),
     path('profile/drafts',DraftListView.as_view(),name='user_drafts'),
     path('profile/comments',CommentListView.as_view(),name='user_comments'),
     path('profile/comments/delete/<int:pk>',CommentDeleteView.as_view(),name='comment_delete'),
]