from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant
from django.shortcuts import get_object_or_404

class RestaurantOwnerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile.role != 'RestaurantOwner':
            return self.handle_no_permission()

        # Assuming that the restaurant ID is passed as a part of the URL (e.g., <restaurant_id>/edit/)
        restaurant_id = kwargs.get('restaurant_id') or kwargs.get('pk')
        if restaurant_id:
            # Get the restaurant and check if the logged-in user is the owner
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            if restaurant.user != request.user:
                return HttpResponseForbidden('You do not have permission to access this page.')

        return super().dispatch(request, *args, **kwargs)
    
def restaurant_owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        restaurant = Restaurant.objects.get(id=kwargs['restaurant_id'] or kwargs['pk'])
        if request.user != restaurant.user and request.user.profile.role != 'RestaurantOwner':
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view