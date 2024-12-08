from django.db import models
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=320, unique=True)
    address = models.CharField(max_length=160)
    
    def __str__(self):
        return self.user.username
    
class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='menu_images', blank=True)
    category = models.CharField(max_length=1, choices=CATEGORIES)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    categories = models.CharField(max_length=1, choices=CATEGORIES)
    image = models.ImageField(upload_to='restaurant_images', blank=True)
    menu = models.ManyToManyField(Menu)
    orders_history = models.ManyToManyField('Order', blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    status = models.CharField(max_length=1, choices=STATUS)
    date = models.DateField()
    total = models.DecimalField(max_digits=5, decimal_places=2)
    menu = models.ManyToManyField(Menu)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
