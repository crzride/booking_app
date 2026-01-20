from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField




class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField (region=None,blank=True,null=True)

    def __str__(self):
        return f"{self.username}"
