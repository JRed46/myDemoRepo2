from django import forms
from .models import audio_object, audioCategories, playlist, PlaylistMapping


class audio_object_form(forms.ModelForm):  
    '''
    Form to create a new audio_object. 

    Fields:
        title (str) : title for the audio file
        category (str) : an option from the choices defined in audioCategories.choices
        file (str) : the file associated with the audio_object
    '''
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title', 'name':'title'}))
    category = forms.CharField(max_length=50, widget=forms.Select(attrs={'class': 'form-input', 'placeholder': 'Category', 'name':'category'}, choices=audioCategories.choices))
    file = forms.FileInput(attrs={'class':'form-input', 'label':'File', 'name':'file'})
    class Meta:  
        model = audio_object  
        fields = ['title', 'category', 'file'] 


class playlist_form(forms.ModelForm):
    '''
    Form to create a new playlist. Note this form does not include the owner attribute.
    In the view function we add the request user as the owner.

    Fields:
        name (str) : name for the playlist
    '''
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Playlist Name', 'name':'name'}))
    class Meta:  
        model = playlist
        fields = ['name'] 


class add_to_playlist_form(forms.ModelForm):
    '''
    Form to add an audio_object to a playlist. The allowed playlists is restricted to
    playlists that exist and are owned by the request user. The form must get the user
    object in order to create an instance, hence the init method. The file is excluded
    since it is added by its pk in the view function. 

    Fields:
        sourcePlaylist (playlist) : foreign key of the playlist object to add the file to.
    '''
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.sourcePlaylist =  forms.ModelChoiceField(queryset=playlist.objects.filter(owner=user)) 
        super(add_to_playlist_form, self).__init__(*args, **kwargs)       

    @staticmethod
    def label_from_instance(obj):
        return obj.name

    class Meta:
        model= PlaylistMapping
        exclude = ["file"]   
        fields = ['sourcePlaylist'] 