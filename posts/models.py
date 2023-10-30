from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum

User = get_user_model()


class SNSType(Enum):
    FACEBOOK = 'facebook'
    INSTAGRAM = 'instagram'
    THREAD = 'thread'
    TWITTER = 'twitter'


class Posts(models.Model):
    content_id = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=[(sns, sns.value) for sns in SNSType])
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)



class HashTags(models.Model):
    name = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

