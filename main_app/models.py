from django.db import models
from django.contrib.auth.models import User

# Category choices
CATEGORIES = (
    ('A', 'Appetizer'),
    ('B', 'Beverage'),
    ('D', 'Dessert'),
    ('E', 'Entree'),
    ('M', 'Main'),
    ('S', 'Side'),
    ('O', 'Other'),
)

STATUS = (
    ('P', 'Pending'),
    ('C', 'Completed'),
    ('D', 'Delivered'),
    ('N', 'Not Paid'),
)

class Order(models.Model):
    status = models.CharField(max_length=1, choices=STATUS)
    order_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=7, decimal_places=3)
    items = models.ManyToManyField('Menu', blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.order_date.strftime('%m/%d/%Y %H:%M:%S')

class Category(models.Model):
    code = models.CharField(max_length=1, choices=CATEGORIES, unique=True)
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.get_code_display()

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
        return ", ".join(category.name for category in self.categories.all())

class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/menu/', blank=True, default=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.category.name} - {self.name}'
    
    class Meta:
        ordering = ['category', 'name']
