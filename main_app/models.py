from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Category choices
STATUS = (
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('D', 'Delivered'),
    ('N', 'Not Paid'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=320)
    address = models.CharField(max_length=160, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    total = models.DecimalField(max_digits=7, decimal_places=3, default=0.000)
    items = models.ManyToManyField('Menu', blank=True, default=None)
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.order_date.strftime('%d/%m/%Y %H:%M')

class Category(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    orders_history = models.ManyToManyField(Order, blank=True, default=None)
    image = models.ImageField(upload_to='images/restaurant/', blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def get_categories_display(self):
        return ', '.join([category.name for category in self.categories.all()])
    
    def get_categories(self):
        return [category.name for category in self.categories.all()]
    
    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/menu/', blank=True, default=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")

    def __str__(self):
        return f'{self.category.name} - {self.name}'
    
    def get_absolute_url(self):
        return reverse('menu_detail', args=[str(self.restaurant.id), str(self.id)])
    
    class Meta:
        ordering = ['category', 'name']
