from django.urls import path
from . import views
from .views import RestaurantOwnerSignupView, CustomerSignupView

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.ProfileUpdate.as_view(), name='profile_update'),
    
    path('accounts/login', views.Login.as_view(), name='login'),
    path('accounts/signup/restaurant-owner/', RestaurantOwnerSignupView.as_view(), name='restaurant_owner_signup'),
    path('accounts/signup/customer/', CustomerSignupView.as_view(), name='customer_signup'),
    
    path('restaurant/create', views.RestaurantCreate.as_view(), name='restaurant_create'),
    path('restaurant/<int:restaurant_id>/update', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    path('restaurant/<int:restaurant_id>/delete', views.RestaurantDelete.as_view(), name='restaurant_delete'),
    
    path('restaurant/<int:restaurant_id>/menu', views.detail, name='detail'),
    path('restaurant/<int:restaurant_id>/menu/<int:menu_id>', views.menu_detail, name='menu_detail'),
    path('restaurant/<int:restaurant_id>/menu/create', views.MenuCreate.as_view(), name='menu_create'),
    path('restaurant/<int:restaurant_id>/menu/<int:pk>/update', views.MenuUpdate.as_view(), name='menu_update'),
    path('restaurant/<int:restaurant_id>/menu/<int:pk>/delete', views.MenuDelete.as_view(), name='menu_delete'),
    
    path('cart', views.cart_index, name='cart'),
    path('cart/<int:menu_id>/add', views.cart_add, name='cart_add'),
    path('cart/<int:menu_id>/remove', views.cart_remove, name='cart_remove'),
    path('cart/<int:menu_id>/increment', views.increment_cart_menu, name='increment_cart_menu'),
    path('cart/<int:menu_id>/decrement', views.decrement_cart_item, name='decrement_cart_item'),
    
    path('orders', views.orders, name='order_list'),
    path('order/<int:pk>', views.order_detail, name='order_detail'),
    path('order/create', views.place_order, name='place_order'),
]