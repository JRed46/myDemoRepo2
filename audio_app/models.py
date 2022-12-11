from unittest.util import _MAX_LENGTH
from django.db import models

class audio_object(models.Model):
    NATURE = 'N'
    MEDITATION = 'M'
    GUIDED_MEDITATION = 'GM'
    BREATHING_EXERCISES = 'BE'
    STORIES = 'S'
    CHOICES = [(NATURE, 'Nature'), (MEDITATION, 'Meditation'), (GUIDED_MEDITATION, 'Guided Meditation'),
                (BREATHING_EXERCISES, 'Breathing Exercise'), (STORIES, 'Stories')]

    title = models.CharField(max_length=500)
    category = models.CharField(max_length=500, choices=CHOICES, default=NATURE)
    file = models.FileField(upload_to='audio_files')
