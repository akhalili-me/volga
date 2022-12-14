from django import forms
from . import models

class PostForm(forms.ModelForm):
    publish = forms.BooleanField(required=False)

    class Meta:
        model = models.Post
        fields = ('title','summary','content','header_image','category')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UpdateForm(forms.ModelForm):

    class Meta:
        model = models.Post
        fields = ('title','summary','content','header_image','category')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ('title',)
