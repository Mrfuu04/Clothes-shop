from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    avatar = models.ImageField(upload_to='user_images', blank=True, verbose_name='Аватар')
    age = models.PositiveIntegerField(default=18, verbose_name='Возраст')
    activation_key = models.CharField(max_length=128, blank=True, verbose_name='Ключ активации')
    is_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Ключ истек')
    first_name = models.CharField(max_length=128, blank=True, null=True, unique=False, verbose_name='Имя')
    last_name = models.CharField(max_length=128, blank=True, null=True, unique=False, verbose_name='Фамилия')

    def is_user_key_expires(self):
        if self.is_key_expires <= now() + timedelta(hours=48):
            return False
        return True


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_COICES = ((MALE, 'М'), (FEMALE, 'Ж'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=False, db_index=True, verbose_name='Пользователь')
    about = models.TextField(verbose_name='О себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_COICES, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
