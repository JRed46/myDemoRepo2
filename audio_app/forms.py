from django import forms
from .models import audio_object


class audio_object_form(forms.ModelForm):  
    class Meta:  
        model = audio_object  
        fields = ['title', 'file']  