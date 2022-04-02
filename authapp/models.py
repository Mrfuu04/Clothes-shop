from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_images', blank=True)
    age = models.PositiveIntegerField(default=18)
