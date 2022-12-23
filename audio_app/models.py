from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

class audioCategories(models.TextChoices):
    NATURE_SOUNDS = 'NS'
    GUIDED_MEDITATIONS = 'GM'
    BREATHING_EXERCISES = 'BE'
    STORIES = 'S'
    BINURAL_BEATS = 'BB'
    INDIAN_RAGAS = 'IR'
    MEDITATION_MUSIC = 'MM'
    SHORT_GUIDED_MEDITATION = 'SGM'
    VOCAL_CHANTING = 'VC'


class audio_object(models.Model):
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=500, choices=audioCategories.choices, default=audioCategories.MEDITATION_MUSIC)
    file = models.FileField(upload_to='audio_files')


class playlist(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False) 
    audios = models.ManyToManyField(audio_object, through = 'PlaylistMapping', related_name = 'audio_files', blank = True)
    def __str__(self):
        return self.name


class PlaylistMapping(models.Model):
    file = models.ForeignKey(audio_object, on_delete = models.CASCADE)
    sourcePlaylist = models.ForeignKey(playlist, on_delete = models.CASCADE)