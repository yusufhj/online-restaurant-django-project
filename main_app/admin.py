from django.contrib import admin

# Register your models here.
from .models import Menu, Restaurant, Order

admin.site.register(Menu)
admin.site.register(Restaurant)
admin.site.register(Order)