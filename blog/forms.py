from django import forms
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title','summary','content','header_image')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Post_Category
        fields = ('category',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('content',)

class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ('title',)
