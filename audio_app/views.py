from django.shortcuts import HttpResponseRedirect, render
from .forms import audio_object_form
from .models import audio_object


def index_render(request):
    return render(request, "index.html", {"activeTab":"index"})


def files_list(request):
    all_audio_objects = audio_object.objects.all()
    return render(request, "files.html", {'all_audio_objects': all_audio_objects, "activeTab":"files"})


def file_upload(request):
    '''
    TODO: admin authenticate
    '''
    if request.method == "POST":
        form = audio_object_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, "upload.html", {"activeTab":"upload"})


def file_delete(request, file_id):
    '''
    TODO: admin authenticate, confirm on front end
    '''
    file_to_delete = audio_object.objects.get(id = file_id)
    if file_to_delete:
        file_to_delete.delete()
    return HttpResponseRedirect('/files/')
    