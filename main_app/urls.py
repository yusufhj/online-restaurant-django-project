from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:restaurant_id>/', views.detail, name='detail'),
]