from django.db import models
from django.contrib.auth.models import User

class Profile():
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=320, unique=True)
    address = models.CharField(max_length=150)