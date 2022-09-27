import imp
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser
from django.utils import timezone
from  django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.CharField(max_length=255)
    header_image = models.ImageField(blank=True,upload_to='post/headers')
    created_Date = models.DateTimeField(default=timezone.now())
    published_Date = models.DateTimeField(blank=True,null=True)
    like = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    author = models.ForeignKey(CustomUser, verbose_name=_("Author"), on_delete=models.CASCADE)

    def publish_post(self):
        self.published_Date = timezone.now
        self.save()
    
    def total_Likes(self):
        return self.like.count()

    def get_absolute_url(self):
        return reverse('home')


    def __str__(self):
        return self.title + ' | ' + self.author


class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_Date = models.DateTimeField(default=timezone.now())
    approved_Comment = models.BooleanField(default=False)

    author = models.ForeignKey(CustomUser, verbose_name=_("Author"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE)

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



class Category(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    def get_all(self):
        return self.objects.all


    def __str__(self):
        return self.title

class Post_Category(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


