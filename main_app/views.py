from django.shortcuts import render
from .models import Menu, Restaurant, Order

from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.

def home(req):
    return render(req, 'home.html', {'restaurants': Restaurant.objects.all()})

def detail(req, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(req, 'restaurant/detail.html', {'restaurant': restaurant, 'menus': Menu.objects.filter(restaurant=restaurant)})

def menu_detail(req, restaurant_id, menu_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menu = Menu.objects.get(id=menu_id)
    return render(req, 'menu/menu_detail.html', {'restaurant': restaurant, 'menu': menu})


# CBVs
class RestaurantCreate(CreateView):
    model = Restaurant
    fields = ['name', 'address', 'categories', 'image']
    template_name = 'restaurant/restaurant_form.html'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RestaurantUpdate(UpdateView):
    model = Restaurant
    fields = ['name', 'address', 'categories', 'image']
    template_name = 'restaurant/restaurant_form.html'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RestaurantDelete(DeleteView):
    model = Restaurant
    success_url = '/'
    template_name = 'restaurant/restaurant_confirm_delete.html'
    