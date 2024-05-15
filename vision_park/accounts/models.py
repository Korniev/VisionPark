from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=32, blank=False, unique=True)
    # first_name = models.CharField(max_length=32, required=False)
    # last_name = models.CharField(max_length=32, required=False) 
    email = models.EmailField(max_length=64, blank=False, unique=True)
    phone_number = models.CharField(null=True, unique=True)
    telegram_nickname = models.CharField(max_length=32, blank=True, unique=True)

    # telegram_id = models.CharField(max_length=64, required=False)

    def __str__(self):
        return self.username
