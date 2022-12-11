from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import login, authenticate
from .forms import audio_object_form, register_form
from django.contrib.auth import login, authenticate
from .models import audio_object


def index_render(request):
    return render(request, "index.html", {"activeTab":"index"})

# def login(response):
#     return render(response,"index.html", {"activeTab":"index"})
def about(request):
    return render(request, "about.html")
def sponsors(request):
    return render(request, "sponsors.html")
# def login(request):
#     return render(request, "index.html", {})

def create_account(request):
    if request.method == "POST":
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            #authenticate user then login
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = register_form()
    return render(request, "registration/register.html", {"form": form})

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
    