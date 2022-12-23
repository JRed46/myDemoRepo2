from django.contrib import admin
from .models import audio_object

# Register your models here.
class audioObjectsAdmin(admin.ModelAdmin):
    '''
    Show all files
    '''
    list_display = ( 'title', 'category', 'file')

admin.site.register(audio_object, audioObjectsAdmin)