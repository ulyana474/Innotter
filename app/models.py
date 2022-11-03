from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('innotter.Tag', related_name='pages')

    owner = models.ForeignKey('innotter.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('innotter.User', related_name='follows')