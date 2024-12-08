from django.shortcuts import render
from .models import Menu, Restaurant, Order
# Create your views here.

def home(req):
    return render(req, 'home.html', {'restaurants': Restaurant.objects.all()})

def detail(req, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(req, 'detail.html', {'restaurant': restaurant, 'menus': Menu.objects.filter(restaurant=restaurant)})