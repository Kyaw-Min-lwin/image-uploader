from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Images


class SignUp(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class SaveImage(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']