from django.shortcuts import render
from .models import Menu, Restaurant, Order, Category

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

def add_menu(req, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(req, 'menu/menu_form.html', {'restaurant': restaurant})

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
    template_name = 'restaurant/restaurant_confirm_delete.html'
    success_url = '/'

class MenuCreate(CreateView):
    model = Menu
    fields = ['name', 'description', 'price', 'category', 'image']
    template_name = 'menu/menu_form.html'
    
    def get_form(self, form_class=None):
        # Get the restaurant instance using the restaurant_id from the URL kwargs
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])

        form = super().get_form(form_class)
        # Set the category queryset to the categories of the specific restaurant
        form.fields['category'].queryset = restaurant.categories.all()
        return form

    def form_valid(self, form):
        # Set the restaurant instance on the form before saving
        print(Restaurant.objects.get(id=self.kwargs['restaurant_id']))
        form.instance.restaurant_id = Restaurant.objects.get(id=self.kwargs['restaurant_id']).id
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return Restaurant.objects.get(id=self.kwargs['restaurant_id']).get_absolute_url()

class MenuUpdate(UpdateView):
    model = Menu
    fields = ['name', 'description', 'price', 'category', 'image']
    template_name = 'menu/menu_form.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Restaurant.objects.get(id=self.kwargs['restaurant_id']).categories.all()
        return form

class MenuDelete(DeleteView):
    model = Menu
    template_name = 'menu/menu_confirm_delete.html'
    
    def get_success_url(self):
        return Restaurant.objects.get(id=self.kwargs['restaurant_id']).get_absolute_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_id'] = self.kwargs['restaurant_id']
        return context
    
