from django import forms
from .models import audio_object, audioCategories, playlist, PlaylistMapping

class audio_object_form(forms.ModelForm):  
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title', 'name':'title'}))
    category = forms.CharField(max_length=50, widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Category', 'name':'category'}, choices=audioCategories.choices))
    file = forms.FileInput(attrs={'class':'form-input', 'label':'File', 'name':'file'})
    class Meta:  
        model = audio_object  
        fields = ['title', 'category', 'file'] 

class playlist_form(forms.ModelForm):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Playlist Name', 'name':'name'}))
    class Meta:  
        model = playlist
        exclude = ["user"]  
        fields = ['name'] 

class add_to_playlist_form(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.sourcePlaylist =  forms.ModelChoiceField(queryset=playlist.objects.filter(owner=user)) 

        print(self.sourcePlaylist)
        # print([(userPlaylist.name, userPlaylist) for userPlaylist in playlist.objects.filter(owner=user)])
        # print(audioCategories.choices)
        # self.sourcePlaylist = forms.CharField(max_length=30, widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Playlist', 'name':'sourcePlaylist'}, choices=[( userPlaylist.id, userPlaylist.name) for userPlaylist in playlist.objects.filter(owner=user)]))
        super(add_to_playlist_form, self).__init__(*args, **kwargs)       

    @staticmethod
    def label_from_instance(obj):
        return obj.name

    class Meta:
        model= PlaylistMapping
        exclude = ["file"]   
        fields = ['sourcePlaylist'] 