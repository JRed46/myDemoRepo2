from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class register_form(UserCreationForm): 
    '''
    Form to create an account. Overrides the default UserCreationForm to use the placeholders
    and other specifics we want on the front end. 
    ''' 
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}))
    firstname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-input'}))
    lastname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-input'}))
    
    class Meta:  
        model =  User
        fields = ['username', 'firstname', 'lastname', 'email', 'password1', 'password2']  

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-input'}),
        }



class login_form(AuthenticationForm):  
    '''
    Form to authenticate users. Overrides the default AuthenticationForm to use the placeholders
    and other specifics we want on the front end. Additionally has methods to login users
    and populate error message.
    ''' 
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user