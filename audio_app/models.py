from unittest.util import _MAX_LENGTH
from django.db import models

class audio_object(models.Model):
    NATURE_SOUNDS = 'NS'
    GUIDED_MEDITATIONS = 'GM'
    BREATHING_EXERCISES = 'BE'
    STORIES = 'S'
    BINURAL_BEATS = 'BB'
    INDIAN_RAGAS = 'IR'
    MEDITATION_MUSIC = 'MM'
    SHORT_GUIDED_MEDITATION = 'SGM'
    VOCAL_CHANTING = 'VC'
    
    CHOICES = [(NATURE_SOUNDS, 'Nature Sounds'), (GUIDED_MEDITATIONS, 'Guided Meditation'), 
               (BREATHING_EXERCISES, 'Breathing Exercises'), (STORIES, 'Stories'),
               (BINURAL_BEATS, 'Binural Beats'), (INDIAN_RAGAS, 'Indian Ragas'),
               (MEDITATION_MUSIC, 'Meditation Music'), (SHORT_GUIDED_MEDITATION, 'Short Guided Mediations'),
               (VOCAL_CHANTING, 'Vocal Chanting')]

    title = models.CharField(max_length=500)
    category = models.CharField(max_length=500, choices=CHOICES, default=MEDITATION_MUSIC)
    file = models.FileField(upload_to='audio_files')
