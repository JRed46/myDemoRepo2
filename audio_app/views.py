from django.shortcuts import HttpResponseRedirect, render
from .forms import audio_object_form
from .models import audio_object


def index_render(request):
    return render(request, "home/index.html", {"activeTab":"index"})


def about(request):
    return render(request, "home/about.html", {"activeTab":"about"})


def background(request):
    return render(request, "home/background.html", {"activeTab":"background"})


def sponsors(request):
    return render(request, "home/sponsors.html", {"activeTab":"sponsors"})


def disclaimer(request):
    return render(request, "home/disclaimer.html", {"activeTab":"disclaimer"})


def instructions(request):
    return render(request, "home/instructions.html", {"activeTab":"instructions"})


def files_list(request):
    all_audio_objects = audio_object.objects.all()
    return render(request, "files.html", {'all_audio_objects': all_audio_objects, "activeTab":"files"})


def file_upload(request):
    '''
    TODO: admin authenticate
    '''
    all_audio_objects = audio_object.objects.all()
    if request.method == "POST":
        form = audio_object_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, "upload.html", {'all_audio_objects': all_audio_objects, "activeTab":"upload"})


def file_delete(request, file_id):
    '''
    TODO: admin authenticate, confirm on front end
    '''
    file_to_delete = audio_object.objects.get(id = file_id)
    if file_to_delete:
        file_to_delete.delete()
    return HttpResponseRedirect('/files/')
    