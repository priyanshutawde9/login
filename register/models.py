from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from register.managers import MyAccountManager

# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=150) 
    employee_id = models.CharField(max_length=200, null=True, unique=True)
    registration_token = models.CharField(max_length=255, blank=True, null=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','employee_id'] #employee_id, token

    objects = MyAccountManager()
    