from django.shortcuts import render
from .models import Menu, Restaurant, Order
# Create your views here.

def home(req):
    return render(req, 'home.html', {'restaurants': Restaurant.objects.all()})

def detail(req, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(req, 'detail.html', {'restaurant': restaurant, 'menus': Menu.objects.filter(restaurant=restaurant)})

def menu_detail(req, restaurant_id, menu_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menu = Menu.objects.get(id=menu_id)
    return render(req, 'menu/menu_detail.html', {'restaurant': restaurant, 'menu': menu})