from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from audio_app.views import *
from .views import create_account, log_in

urlpatterns = [
    # Auth URLs
    path("register/", create_account, name="register"),
    path("login/", log_in, name="login"),
    path('', include("django.contrib.auth.urls")), ## logout url

    # Home URLs
    path("", index_render, name="index"),
    path("about/", about_render, name="about"),
    path("background/", background_render, name="background"),
    path("sponsors/", sponsors_render, name="sponsors"),
    path("instructions/", instructions_render, name="instructions"),
    path("disclaimer/", disclaimer_render, name="disclaimer"),

    # Chatbot URLs
    path("chatbot/", chatbot_render, name="chatbot"),

    # General Listen URLs
    path("listen/", listen_landing, name="listen"),
    path("listen/<str:category>", listen_category, name="listen_category"),
    path("upload/", file_upload, name="upload"),
    path("delete_file/<str:category>/<int:file_id>", file_delete, name="delete"),

    # Playlist URLs
    path("createPlaylist/", createPlaylist, name="createPlaylist"),
    path("deletePlaylist/<int:playlistId>", deletePlaylist, name="deletePlaylist"),
    path("listen/playlist/<int:playlistId>", listenPlaylist, name="listenPlaylist"),
    path("addToPlaylist/<int:fileId>/<str:fileName>", addToPlaylist, name="addToPlaylist"),
    path("removeFromPlaylist/<int:playlistId>/<int:fileId>", removeFromPlaylist, name="removeFromPlaylist"),

    # Admin 
    path("admin/manageSubmissions/", manageSubmissions, name='manageSubmissions'),
    path("admin/approveSubmission/<int:fileId>", approveSubmission, name='approveSubmission'),
    path("admin/denySubmission/<int:fileId>", denySubmission, name='denySubmission'),
    path("admin/superuser/", admin.site.urls), # include django admin interface for superusers
]


# Only add this when we in debug mode and do not have nginx to serve these items
# Serves media and atatic files through django when Nginx is not running to serve them
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)