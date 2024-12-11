from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Menu, Restaurant, Order, Category, Profile, MenuOrder

admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(MenuOrder)
