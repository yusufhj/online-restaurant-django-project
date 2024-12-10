from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('You do not have access to this page.')
        return _wrapped_view
    return decorator

class GroupRequiredMixin(LoginRequiredMixin):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.groups.filter(name=self.group_required).exists():
            return HttpResponseForbidden('You do not have access to this page.')
        return super().dispatch(request, *args, **kwargs)