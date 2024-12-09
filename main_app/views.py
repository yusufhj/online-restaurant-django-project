from django.shortcuts import render, redirect
from .models import Menu, Restaurant, Order, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def signup(req):
    error_message = ''
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(req, 'registration/signup.html', context)

class Login(LoginView):
    template_name = 'registeration/login.html'


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

def cart_index(req):
    return render(req, 'cart/index.html', 
                  {'orders': Order.objects.filter(user=req.user)}
                  )

# CBVs
class RestaurantCreate(LoginRequiredMixin, CreateView):
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
