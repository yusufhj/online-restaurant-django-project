from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant/<int:restaurant_id>/menu', views.detail, name='detail'),
    path('restaurant/<int:restaurant_id>/menu/<int:menu_id>', views.menu_detail, name='menu_detail'),
]