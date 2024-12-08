from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User
# Create your models here.

CATEGORIES = (
    ('A', 'Appetizer'),
    ('E', 'Entree'),
    ('M', 'Main'),
    ('S', 'Side'),
    ('D', 'Dessert'),
    ('B', 'Beverage'),
    ('O', 'Other')
)

STATUS = (
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('D', 'Delivered'),
    ('N', 'Not Paid')
)

class Order(models.Model):
    status = models.CharField(max_length=1, choices=STATUS)
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=3)
    items = models.ManyToManyField('Menu', blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    categories = ArrayField(models.CharField(max_length=1, choices=CATEGORIES))
    image = models.ImageField(upload_to='restaurant_images', blank=True, default=None)
    orders_history = models.ManyToManyField(Order, blank=True, default=None)
    
    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='menu_images', blank=True, default=None)
    category = models.CharField(max_length=1, choices=CATEGORIES)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


