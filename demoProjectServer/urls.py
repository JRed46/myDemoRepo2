from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import create_account, log_in, homePageRender
from tasks.views import *

urlpatterns = [
    # chat urls
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
    # tasks urls
    path('tasks/list/', task_list, name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/detail/<int:task_id>/', task_detail, name='task_detail'),
    path('tasks/complete/<int:task_id>/', task_complete, name='task_complete'),
    path('tasks/delete/<int:task_id>/', task_delete, name='task_delete'),
    # Auth URLs
    path("register/", create_account, name="register"),
    path("login/", log_in, name="login"),
    path("", homePageRender, name="index"),
    path('', include("django.contrib.auth.urls")), ## logout url
    path("admin/superuser/", admin.site.urls), # include django admin interface for superusers
]


# Only add this when we in debug mode and do not have nginx to serve these items
# Serves media and atatic files through django when Nginx is not running to serve them
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)