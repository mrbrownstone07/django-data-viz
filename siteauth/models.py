from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date


class User(AbstractUser):
    
    class Meta:
        verbose_name = 'Site User'
        verbose_name_plural = 'Site Users'
    
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(unique = True)
    phone_no = models.CharField(max_length = 10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    
    def __str__(self):
        return "{}".format(self.email)
