from unittest.util import _MAX_LENGTH
from django.db import models

class audio_object(models.Model):
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to='audio_files')
