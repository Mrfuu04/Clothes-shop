from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
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


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_COICES = ((MALE, 'М'), (FEMALE, 'Ж'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False, db_index=True)
    about = models.TextField(verbose_name='О себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_COICES, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
