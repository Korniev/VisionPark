from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=32, blank=False, unique=True)
    email = models.EmailField(max_length=64, blank=False, unique=True)
    phone_number = models.CharField(null=True, unique=True)
    telegram_nickname = models.CharField(max_length=32, blank=True, unique=True)

    def __str__(self):
        return self.username
