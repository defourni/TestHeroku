from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

VISIBILITY_CHOICES = [(1, "public"), 
                      (2, "private"),
                      (3, "friends"), 
                      (4, "friends and friends of friends"), 
                      (5, "another author"), 
                      (6, "friends on the same host"), ]
TEXT_TYPE_CHOICES = [(1, "plaintext"),
                     (2, "markdown"),]

class Post(models.Model):
    # id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, default=1, related_name="post_author")
    content = models.TextField(blank=True, max_length=2000)
    origin_post = models.ForeignKey('self', on_delete = models.CASCADE, blank=True, null=True)      # link of the commented post
    text_type = models.IntegerField(choices=TEXT_TYPE_CHOICES, default='1')
    add_time = models.DateTimeField(auto_now_add = True)        # time of the post created
    mod_time = models.DateTimeField(auto_now = True)            # time of the post modified
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default='1')
    another_author = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name="another_author")
    unlist = models.BooleanField(default=False)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, default=1)
    # order = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to='uploads', blank=False)