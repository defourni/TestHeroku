from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

USER_TYPES = [("author", "Author"), 
              ("admin", "Admin"),]

# see more: https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.TextField(choices=USER_TYPES, default='author', max_length=10)
    approved = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='uploads', blank=True)
    github = models.URLField(max_length=100, null=False, blank=True) #author github address

# class User(AbstractUser):
#     username = models.CharField(blank=False, null=True, unique=True)
#     # email = models.EmailField(_('email address'), unique=True)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     def __str__(self):
#         return "{}".format(self.username)

# class Author(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     user_type = models.IntegerField(choices=USER_TYPES, default='1')
#     approved = models.BooleanField(default=False)
#     avatar = models.ImageField(upload_to='uploads', blank=True)
#     github = models.URLField(max_length=100, null=False, blank=True) #author github address