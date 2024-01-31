from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from .models import Customuser


class Emailbackend(ModelBackend):
    def authenticate(self,username = None , password = None, **kwargs):
        Usermodel = get_user_model()
        try:
            user = Customuser.objects.get(email = username)
            if user.check_password(password):
                return user
        except Customuser.DoesNotExist: 
            return None
