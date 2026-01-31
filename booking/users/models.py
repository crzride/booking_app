from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField




class User(AbstractUser):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField(unique=True)
    phone = PhoneNumberField (region=None,blank=True,null=True, unique=True)
    country = models.CharField(default='null', max_length=30, blank=False)
    sex = models.CharField(choices=SEX, max_length=10, default='M')

    def __str__(self):
        return f"{self.username}"
