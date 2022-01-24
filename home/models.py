from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, primary_key=True, unique=True)
    unique_id = models.CharField(max_length=25)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)
    is_verified_user = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile/pic')
    profile_pic_path = models.CharField(max_length=1000, default=f'{settings.MEDIA_URL}profile/pic/default_profile_pic.png')
    profile_create_date = models.DateTimeField(auto_now=True)
    right_to_post = models.BooleanField(default=True)
    right_to_like_post = models.BooleanField(default=True)
    right_to_change_profile_pic = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Item(models.Model):
    uuid = models.CharField(max_length=25, default=None)
    item_id = models.CharField(max_length=25, default=None)
    name = models.CharField(max_length=100, default=None)
    path = models.CharField(max_length=1000,  default=f'{settings.MEDIA_URL}items/')
    category = models.CharField(max_length=50, default='image')
    subcategory = models.CharField(max_length=50, default='others')
    likes = models.IntegerField(default=1)
    right_to_like = models.BooleanField(default=True)
    search_tags = models.TextField(max_length=150, default='')
    searchable = models.BooleanField(default=True)
    in_search = models.BooleanField(default=False)
    downloads_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    liked_by = models.TextField(default='')

    def __str__(self):
        return self.name

class Uploads(models.Model):
    uuid = models.CharField(max_length=25, default=None)
    uploaded = models.TextField(default='')

    def __str__(self):
        return self.uuid

class Downloads(models.Model):
    uuid = models.CharField(max_length=25, default=None)
    downloaded = models.TextField(default='')

    def __str__(self):
        return self.uuid

class Liked(models.Model):
    uuid = models.CharField(max_length=25, default=None)
    liked= models.TextField(default='')

    def __str__(self):
        return self.uuid