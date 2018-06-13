from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    tag = models.ManyToManyField(Tag)
    pub_time = models.DateTimeField('time published', default=timezone.now)
    title = models.CharField(max_length=40)
    text = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField()
    pub_time = models.DateTimeField('time published', default=timezone.now)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    alias = models.CharField(max_length=30, default=None, null=True, blank=True)

    def __str__(self):
        return self.text


class Image(models.Model):
    url = models.URLField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=300, default=None, null=True, blank=True)
    name = models.CharField(max_length=50, default="default")

    def __str__(self):
        return self.name
