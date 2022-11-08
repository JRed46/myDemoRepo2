from operator import index
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from audio_app.views import *

urlpatterns = [
    path("", index_render, name="index"),
    path("files/", files_list, name="files"),
    path("upload/", file_upload, name="upload"),
    path("delete_file/<int:file_id>", file_delete, name="delete"),
    path("admin/", admin.site.urls),
]

# Only add this when we in debug mode and do not have nginx to serve these items
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)