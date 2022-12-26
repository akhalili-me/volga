from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect('/')


class AuthorCheckMixin(UserPassesTestMixin):
    
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user 
        
    def handle_no_permission(self):
        return redirect('/')



