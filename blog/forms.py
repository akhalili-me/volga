from django import forms
from . import models

class PostForm(forms.ModelForm):
    publish = forms.BooleanField(required=False)

    class Meta:
        model = models.Post
        fields = ('title','summary','content','header_image')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

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
