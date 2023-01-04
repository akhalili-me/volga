from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from django.utils import timezone
from  django.urls import reverse
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)
post_image = PathAndRename('post/headers')
category_image = PathAndRename('post/category')

#########################
#########################

class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True,upload_to=category_image)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(max_length=255)
    header_image = models.ImageField(blank=True,upload_to=post_image)
    created_Date = models.DateTimeField(default=timezone.now())
    published_Date = models.DateTimeField(blank=True,null=True)
    like = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    author = models.ForeignKey(CustomUser, verbose_name=_("Author"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE)

    def publish_post(self):
        self.published_Date = timezone.now()
        self.save()
    
    def total_Likes(self):
        return self.like.count()

    def get_absolute_kurl(self):
        return reverse('blog:post',kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ' | ' + self.author.email


class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_Date = models.DateTimeField(default= timezone.now())
    approved_Comment = models.BooleanField(default=True)

    author = models.ForeignKey(CustomUser, verbose_name=_("Author"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"),related_name='comments', on_delete=models.CASCADE)

    def approve(self):
        self.approved_Comment = True
        self.save

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.content

class Tag(models.Model):
    title = models.CharField(max_length=50)
    count = models.IntegerField()

    def __str__(self):
        return self.title

class Post_Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
