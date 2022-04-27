from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.utils.timezone import now


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_images', blank=True)
    age = models.PositiveIntegerField(default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    is_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)
    first_name = models.CharField(max_length=128, blank=True, null=True, unique=False)
    last_name = models.CharField(max_length=128, blank=True, null=True, unique=False)

    def is_user_key_expires(self):
        if self.is_key_expires <= now() + timedelta(hours=48):
            return False
        return True
