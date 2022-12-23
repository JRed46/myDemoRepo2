from django.contrib import admin
from .models import audio_object, playlist

# Register your models here.
class audioObjectsAdmin(admin.ModelAdmin):
    '''
    Show all files
    '''
    list_display = ( 'title', 'category', 'file')

# Register your models here.
class playlistAdmin(admin.ModelAdmin):
    '''
    Show all files
    '''
    list_display = ( 'name', 'owner')

admin.site.register(audio_object, audioObjectsAdmin)
admin.site.register(playlist, playlistAdmin)