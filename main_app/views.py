from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# from .forms import UserRegisterForm
from .models import Menu, Restaurant, Order, Category, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .decorators import RestaurantOwnerRequiredMixin, restaurant_owner_required

class Login(LoginView):
    template_name = 'registeration/login.html'


def home(req):
    return render(req, 'home.html', {'restaurants': Restaurant.objects.all()})

@login_required
def profile(req):
    return render(req, 'profile/detail.html', {'restaurants': Restaurant.objects.all()})

@login_required
def detail(req, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    
    return render(req, 'restaurant/detail.html', {'restaurant': restaurant, 'menus': Menu.objects.filter(restaurant=restaurant)})

@login_required
def menu_detail(req, restaurant_id, menu_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menu = Menu.objects.get(id=menu_id)
    return render(req, 'menu/menu_detail.html', {'restaurant': restaurant, 'menu': menu})

@login_required
@restaurant_owner_required
def add_menu(req, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(req, 'menu/menu_form.html', {'restaurant': restaurant})

@login_required
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

@login_required
def cart_add(req, menu_id):
    cart = req.session.get('cart', {})
    # if item already exists in cart, increment by 1
    if str(menu_id) in cart:
        cart[str(menu_id)] = cart[str(menu_id)] + 1
    else:
        cart[menu_id] = cart.get(menu_id, 0) + 1 
    
    req.session['cart'] = cart
    return redirect('/cart')

@login_required
def cart_remove(req, menu_id):
    cart = req.session.get('cart', {})
    # if item already exists in cart, increment by 1
    if str(menu_id) in cart:
        del cart[str(menu_id)]
    
    req.session['cart'] = cart
    return redirect('/cart')

@login_required
def increment_cart_menu(req, menu_id):
    cart = req.session.get('cart', {})
    # increment by 1
    cart[str(menu_id)] = cart[str(menu_id)] + 1
    
    req.session['cart'] = cart
    return redirect('/cart')

@login_required
def decrement_cart_item(req, menu_id):
    cart = req.session.get('cart', {})
    cart[str(menu_id)] = cart[str(menu_id)] - 1
    # if item quantity is 0, remove item
    if cart[str(menu_id)] <= 0:
        del cart[str(menu_id)]
    
    req.session['cart'] = cart
    return redirect('/cart')

@login_required
def place_order(req):
    session_cart = req.session.get('cart', {})
    order = Order(user=req.user)
    order.save()
    
    for cart_item_id in session_cart:
        item = Menu.objects.get(id=cart_item_id)
        order.items.add(item)
    
    order.total = sum([item.price * session_cart[str(item.id)] for item in order.items.all()])
    order.save()
    
    req.session['cart'] = {}
    return redirect('/orders')

@login_required
def orders(req):
    orders = Order.objects.filter(user=req.user)
    return render(req, 'order/index.html', {'orders': orders})

@login_required
def order_detail(req, pk):
    order = Order.objects.get(id=pk)
    if order.user != req.user:
        return redirect('/orders')
    return render(req, 'order/detail.html', {'order': order})

# CBVs
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['address']
    template_name = 'profile/profile_form.html'
    success_url = '/profile'
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    


class RestaurantCreate(RestaurantOwnerRequiredMixin, CreateView):
    model = Restaurant
    fields = ['name', 'address', 'categories', 'image']
    template_name = 'restaurant/restaurant_form.html'
    success_url = '/'
    group_required = 'RestaurantOwner'
    
    def form_valid(self, form):
        if self.request.user.profile.role != 'RestaurantOwner':
            return redirect('/')
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class RestaurantUpdate(RestaurantOwnerRequiredMixin, UpdateView):
    model = Restaurant
    fields = ['name', 'address', 'categories', 'image']
    template_name = 'restaurant/restaurant_form.html'
    success_url = '/'
    group_required = 'RestaurantOwner'
    
    def form_valid(self, form):
        if self.request.user.profile.role != 'RestaurantOwner' or self.request.user != form.instance.user:
            return redirect('/') 

        form.instance.user = self.request.user
        return super().form_valid(form)


class RestaurantDelete(RestaurantOwnerRequiredMixin, DeleteView):
    model = Restaurant
    template_name = 'restaurant/restaurant_confirm_delete.html'
    success_url = '/'
    group_required = 'RestaurantOwner'

    def check_user(self):
        if self.request.user.profile.role != 'RestaurantOwner' or self.request.user != Restaurant.objects.get(id=self.kwargs['pk']).user:
            return redirect('/')
    


class MenuCreate(RestaurantOwnerRequiredMixin, CreateView):
    model = Menu
    fields = ['name', 'description', 'price', 'category', 'image']
    template_name = 'menu/menu_form.html'
    group_required = 'RestaurantOwner'
    
    def get_form(self, form_class=None):
        # Get the restaurant instance using the restaurant_id from the URL kwargs
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_id'])

        form = super().get_form(form_class)
        # Set the category queryset to the categories of the specific restaurant
        form.fields['category'].queryset = restaurant.categories.all()
        return form

    def form_valid(self, form):
        # Set the restaurant instance on the form before saving
        if self.request.user.profile.role != 'RestaurantOwner' or self.request.user != Restaurant.objects.get(id=self.kwargs['restaurant_id']).user:
            return redirect('/')
        
        print(Restaurant.objects.get(id=self.kwargs['restaurant_id']))
        form.instance.restaurant_id = Restaurant.objects.get(id=self.kwargs['restaurant_id']).id
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return Restaurant.objects.get(id=self.kwargs['restaurant_id']).get_absolute_url()


class MenuUpdate(RestaurantOwnerRequiredMixin, UpdateView):
    model = Menu
    fields = ['name', 'description', 'price', 'category', 'image']
    template_name = 'menu/menu_form.html'
    group_required = 'RestaurantOwner'
    
    def get_form(self, form_class=None):
        if self.request.user.profile.role != 'RestaurantOwner' or self.request.user != Restaurant.objects.get(id=self.kwargs['restaurant_id']).user:
            return redirect('/')
        form = super().get_form(form_class)
        form.fields['category'].queryset = Restaurant.objects.get(id=self.kwargs['restaurant_id']).categories.all()
        return form

class MenuDelete(RestaurantOwnerRequiredMixin, DeleteView):
    model = Menu
    template_name = 'menu/menu_confirm_delete.html'
    group_required = 'RestaurantOwner'
    
    def get_success_url(self):
        return Restaurant.objects.get(id=self.kwargs['restaurant_id']).get_absolute_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant_id'] = self.kwargs['restaurant_id']
        return context
    
    def check_user(self):
        if self.request.user.profile.role != 'RestaurantOwner' or self.request.user != Restaurant.objects.get(id=self.kwargs['restaurant_id']).user:
            return redirect('/')


from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import RestaurantOwnerSignupForm, CustomerSignupForm
from django.contrib.auth.models import Group

class RestaurantOwnerSignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = RestaurantOwnerSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()  # Save the user instance

        profile = user.profile
        profile.role = 'RestaurantOwner'
        profile.save()

        login(self.request, user)
        return super().form_valid(form)


class CustomerSignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomerSignupForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()  # Save the user instance

        profile = user.profile
        profile.role = 'Customer'
        profile.save()

        login(self.request, user)
        return super().form_valid(form)
