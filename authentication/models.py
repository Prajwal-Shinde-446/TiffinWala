from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core import validators
from django.contrib.auth.models import Permission



class CustomUserManager(BaseUserManager):

    def create_user(self, password=None ,email = None , *args, **kwargs):
        if not email:
            return ValueError("The Email is a required field to register")
        user = self.model(email=email , *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'superuser')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Customuser(AbstractUser , PermissionsMixin):

    User_Type = (
        ('subscribed','Subscribed'),
        ('user','User'),
        ('superuser','Superuser')
    )
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_user_permissions'
    )
    user_type = models.CharField(choices=User_Type,max_length=50,default='user')
    name = models.CharField(max_length=50, null = False, blank = False)
    phone = models.CharField(max_length=13, validators=[validators.MinLengthValidator(10)], null = False, blank = False)
    profile_picture = models.ImageField(upload_to='images/', null = True, blank = True)
    email = models.EmailField( null = False, blank = False, unique = True)
    email_verified = models.BooleanField(default = False)
    email_otp = models.CharField(max_length = 4 ,null = True )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    