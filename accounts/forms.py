from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile

class CustomUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','email','password1','password2']


class UpdateProfile(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['phone_number','address']
        