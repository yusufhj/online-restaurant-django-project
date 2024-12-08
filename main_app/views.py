from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegisterForm
from .models import Menu, Restaurant, Order, Category, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class Login(LoginView):
    template_name = 'registeration/login.html'


def home(req):
    return render(req, 'home.html', {'restaurants': Restaurant.objects.all()})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserRegisterForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def profile(req):
    return render(req, 'profile/detail.html', {'restaurants': Restaurant.objects.all()})

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
    session_cart = req.session.get('cart', {})
    print('---------------------------------', session_cart)
    cart = []
    # get all items with the stored id
    for cart_item_id in session_cart:
        item = Menu.objects.get(id=cart_item_id)
        # set quantity and total for each item
        item.quantity = session_cart[str(item.id)]
        item.total = item.price * item.quantity
        
        cart.append(item)
    
    return render(req, 'cart/index.html', 
                  {'cart': cart}
                  )

def cart_add(req, menu_id):
    cart = req.session.get('cart', {})
    # if item already exists in cart, increment by 1
    if str(menu_id) in cart:
        cart[str(menu_id)] = cart[str(menu_id)] + 1
    else:
        cart[menu_id] = cart.get(menu_id, 0) + 1 
    
    req.session['cart'] = cart
    return redirect('/cart')

def cart_remove(req, menu_id):
    cart = req.session.get('cart', {})
    # if item already exists in cart, increment by 1
    if str(menu_id) in cart:
        del cart[str(menu_id)]
    
    req.session['cart'] = cart
    return redirect('/cart')

def increment_cart_menu(req, menu_id):
    cart = req.session.get('cart', {})
    # increment by 1
    cart[str(menu_id)] = cart[str(menu_id)] + 1
    
    req.session['cart'] = cart
    return redirect('/cart')
    
def decrement_cart_item(req, menu_id):
    cart = req.session.get('cart', {})
    cart[str(menu_id)] = cart[str(menu_id)] - 1
    # if item quantity is 0, remove item
    if cart[str(menu_id)] <= 0:
        del cart[str(menu_id)]
    
    req.session['cart'] = cart
    return redirect('/cart')
    
    
# CBVs
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['address',]
    template_name = 'profile/profile_form.html'
    success_url = '/profile/'
    
    # if user is trying to edit another user information, redirect to home page
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if pk != self.request.user.id:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

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