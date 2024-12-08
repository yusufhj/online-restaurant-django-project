from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Menu, Restaurant, Order, Profile

admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Profile)