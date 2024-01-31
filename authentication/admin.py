from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class Usermodel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(Customuser,Usermodel)