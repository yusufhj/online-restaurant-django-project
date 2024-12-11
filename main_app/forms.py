from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.models import Group

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# # Create a UserUpdateForm to update a username and email
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email']


class RestaurantOwnerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = Group.objects.get(name='RestaurantOwner')
            user.groups.add(group)
        return user

class CustomerSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
        return user