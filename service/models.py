from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.core import validators
from authentication.models import CustomUserManager,Customuser

# Create your models here.

class Service():

    service_name = models.CharField(max_length=50, null = False, blank = False)
    service_phone = models.CharField(max_length=13, validators=[validators.MinLengthValidator(10)], null = False, blank = False)
    profile_picture = models.ImageField(upload_to='images/', null = True, blank = True)
    ownwer_contact = models.CharField(max_length = 10 , null = False , blank = False)
    user = models.ForeignKey(Customuser , on_delete=models.CASCADE,unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email