from django import forms
from .models import audio_object
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class audio_object_form(forms.ModelForm):  
    class Meta:  
        model = audio_object  
        fields = ['title', 'file']  


## override UsercreationForm with register_form
class register_form(UserCreationForm):  
    firstname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-input'}))
    lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-input'}))
    
    class Meta:  
        model =  User
        fields = ['firstname', 'lastname', 'email', 'password1', 'password2']  

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-input'}),
        }