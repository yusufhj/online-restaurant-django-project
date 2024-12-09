from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant/create', views.RestaurantCreate.as_view(), name='restaurant_create'),
    path('restaurant/<int:pk>/update', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    path('restaurant/<int:pk>/delete', views.RestaurantDelete.as_view(), name='restaurant_delete'),
    
    path('restaurant/<int:restaurant_id>/menu', views.detail, name='detail'),
    path('restaurant/<int:restaurant_id>/menu/<int:menu_id>', views.menu_detail, name='menu_detail'),
    
    path('restaurant/<int:restaurant_id>/menu/create', views.MenuCreate.as_view(), name='menu_create'),
    path('restaurant/<int:restaurant_id>/menu/<int:pk>/update', views.MenuUpdate.as_view(), name='menu_update'),
    path('restaurant/<int:restaurant_id>/menu/<int:pk>/delete', views.MenuDelete.as_view(), name='menu_delete'),
]