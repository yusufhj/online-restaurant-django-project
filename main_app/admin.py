from django.contrib import admin

# Register your models here.
from .models import Menu, Restaurant, Order, Category

admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(Category)