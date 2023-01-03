from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User


#########
# FILES #
#########


class audioCategories(models.TextChoices):
    '''
    Sets the category abbreviations for audio_objects
    '''
    NATURE_SOUNDS = 'NS'
    GUIDED_MEDITATIONS = 'GM'
    BREATHING_EXERCISES = 'BE'
    STORIES = 'S'
    BINAURAL_BEATS = 'BB'
    INDIAN_RAGAS = 'IR'
    MEDITATION_MUSIC = 'MM'
    SHORT_GUIDED_MEDITATION = 'SGM'
    VOCAL_CHANTING = 'VC'


class audio_object(models.Model):
    '''
    Files in the library. In addition to the actual file, the object stores a title and category
    selected from audioCategories. Approved is set by default to False- anyone can submit a file
    so we need to vet the before serving. 
    '''
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=500, choices=audioCategories.choices, default=audioCategories.MEDITATION_MUSIC)
    file = models.FileField(upload_to='audio_files')
    approved=models.BooleanField(default=False)




#############
# PLAYLISTS #
#############


class playlist(models.Model):
    '''
    User created playlist. Playlists have a name that is displayed and an owner user
    that we use to retrieve user playlists and check if playlist CRUD operations are
    allowed. audios is a manyToMany field that maps to the the playlist files stored in
    the PlaylistMapping model. See the documentation on many to many relationships for
    more information: https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_many/

    Also note that when a user deletes their account all their playlists will be deleted 
    automatically from this definition.
    '''
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False) 
    audios = models.ManyToManyField(audio_object, through = 'PlaylistMapping', related_name = 'audio_files', blank = True)

    def __str__(self):
        return self.name


class PlaylistMapping(models.Model):
    '''
    Item in a user created playlist. In the many to many relationship,
    we can use the playlist.audios attribute to go from a playlist to 
    them items, and we includ sourcePlaylist here so we can go from the item
    back to the playlist. A playlist item also of course needs the item itself,
    which is an audio_object stored as a foreign key.

    Note that on deletion of a playlist or a file, the corresponding playlist mapping
    entries will be deleted automatically from this definition. 
    '''
    file = models.ForeignKey(audio_object, on_delete = models.CASCADE)
    sourcePlaylist = models.ForeignKey(playlist, on_delete = models.CASCADE)