from django import forms
from .models import audio_object

CATEGORIES = ['Nature', 'Meditation', 'Guided Meditation', 'Breathing Exercises', 'Stories']
class audio_object_form(forms.ModelForm):  
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'label':'Title', 'name':'title'}))
    category = forms.CharField(max_length=50, label="Category", widget=forms.Select(choices=CATEGORIES))
    file = forms.FileInput(attrs={'class':'form-input', 'label':'File', 'name':'file'})
    class Meta:  
        model = audio_object  
        fields = ['title', 'category', 'file'] 