from django.shortcuts import redirect, render
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

def create_account(response):
    if response.method == "POST":
        form = register_form(response.POST)
        if form.is_valid():
            form.save() # save user in database
        return redirect("/")
    else:
        form = register_form()
    return render(response, "registration/register.html", {"form": form})

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
    return redirect('/files/')
    