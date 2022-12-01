from django import forms
from .models import audio_object, models
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class audio_object_form(forms.ModelForm):  
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'label':'Title', 'name':'title'}))
    file = forms.FileInput(attrs={'class':'form-input', 'label':'File', 'name':'file'})
    class Meta:  
        model = audio_object  
        fields = ['title', 'file'] 


## override UsercreationForm with register_form
class register_form(UserCreationForm):  
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-input', 'label':''}))
    firstname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-input', 'label':''}))
    lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-input', 'label':''}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input', 'label':''}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-input', 'label':''}))
    class Meta:  
        model =  User
        fields = ['firstname', 'lastname', 'username']  
