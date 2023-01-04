from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import audio_object_form, playlist_form, add_to_playlist_form
from .models import audio_object, playlist, PlaylistMapping
from .utils import *
import mutagen



####################
# HOME PAGES VIEWS #    # Simple functions that manage the static home pages
####################


def index_render(request):
    '''
    Rendering function for the index page. Note in this application
    we have a template parameter 'activeTab'. styleActiveTab.js
    will find the element with id=kwargs['activeTab'] and add the 
    class 'active' to it. The styling marks this as the active tab. 
    Be sure to use this when coding new view functions. Corresponding
    url is '/'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered index template
    '''
    return render(request, "home/index.html", {"activeTab":"index"})


def about_render(request):
    '''
    Rendering function for the about page. Corresponding url is '/about'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered about template
    '''
    return render(request, "home/about.html", {"activeTab":"about"})


def background_render(request):
    '''
    Rendering function for the background page. Corresponding url is '/background'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered background template
    '''
    return render(request, "home/background.html", {"activeTab":"background"})


def sponsors_render(request):
    '''
    Rendering function for the sponsors page. Corresponding url is '/sponsors'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered sponsors template
    '''
    return render(request, "home/sponsors.html", {"activeTab":"sponsors"})


def disclaimer_render(request):
    '''
    Rendering function for the disclaimer page. Corresponding url is '/disclaimer'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered disclaimer template
    '''
    return render(request, "home/disclaimer.html", {"activeTab":"disclaimer"})


def instructions_render(request):
    '''
    Rendering function for the instructions page. Corresponding url is '/instructions'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered instructions template
    '''
    return render(request, "home/instructions.html", {"activeTab":"instructions"})




########################
# GENERAL LISTEN VIEWS #    # View and manage all files in library
########################    


def listen_landing(request):
    '''
    Rendering function for the listen landing page. This is the page that users are 
    shown when they click "Browse All" under "Listen" in the topnav. 
    Shows the 9 file categories and lets users click into the categories if they are authenticated. 
    Users do not need authentication to view the page but are redirected to the login page
    instead of the category list if they click a category and are not authenticated.
    Corresponding url is '/listen'.

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered instructions template
    '''
    return render(request, "listen_landing.html", {"activeTab":"listen"})


@login_required(login_url=reverse_lazy('login'))
def listen_category(request, category):
    '''
    Rendering function for the listen by category page. This is the page that users are 
    shown when they click a category from the "Browse All" page. Shows all approved files 
    with that category. Corresponding url is '/listen/{{category}}'. {{category}} is the URL extention used 
    for the page, which maps to a database category attribute via the utility dictionary categoryToAbreviation.
    This mapping lets us have user friendly URLs without uneccesarily long database attributes.
    We then retrieve the files for the category and a title for the page. Note it would be very simple
    to add additional categories. 
    
    This function is also very similar to listenPlaylist, which uses the same 
    template to display a list of playlist audio_objects. The template variabe 'listType' is used by the template
    to determine which actions are allowed in the category view versus playlist view, 
    In the category view these are add to playlist and delete from library (if admin).
    In the playlist view this is instead delete from playlist. 

    Parameters:
        request (http): http GET request
        category (str) : URL friendly name of the category
    
    Returns:
        HttpResponseRedirect: the rendered instructions template
    '''
    audio_objects = audio_object.objects.filter(category = categoryToAbreviation.get(category), approved=True)
    adminUser = is_admin(request.user) # display additional icon to delete file if user is admin
    kwargs = {"activeTab":"listen", 'audio_objects':audio_objects, 'category_title':categoryToTitle.get(category),
              'listType':'category', 'adminUser':adminUser, 'category':category}
    return render(request, "listen_files.html", kwargs)

 
@login_required(login_url=reverse_lazy('login'))
def file_upload(request):
    '''
    Handler function to upload files to the library. In the GET branch, renders
    a form used to submit file uploads. In the POST branch, adds file to library
    if the form is valid. Note audio objects have an attribute "approved". 
    Only objects with "approved" = True are displayed on the front end. This function
    sets the new file to approved if the user is in the admin group or otherwise 
    leaves it not approved until an admin later approves it. 

    Parameters:
        request (http): http GET or POST request
    
    Returns:
        HttpResponseRedirect: back to the upload url to fix errors or submit another file
    '''
    if request.method == "POST":
        form = audio_object_form(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            audio_info = mutagen.File(file.file).info
            file.duration = audio_info.length
            if is_admin(request.user):
                file.approved = True
            file.save()
            return HttpResponseRedirect('/upload/')
    else:
        form = audio_object_form()
    return render(request, "upload.html", {"activeTab":"upload", 'form':form})


@login_required(login_url=reverse_lazy('login'))
def file_delete(request, category, file_id):
    '''
    Handler function to delete files from the library. Checks the file 
    exists and the user is in the admin group, and if so deletes the file
    from the library. Deletion of files cascades into the user playlist to file
    mapping model automatically from the model definition, so no need to manually
    handle that here.  

    Parameters:
        request (http): http GET request
        category (str) : URL friendly name of the category for redirection
        file_id (int) : pk of the file in the audio_object database table

    
    Returns:
        HttpResponseRedirect: back to the source category of the file
    '''
    if is_admin(request.user):
        file_to_delete = audio_object.objects.get(id = file_id)
        if file_to_delete:
            file_to_delete.delete()
    return HttpResponseRedirect('/listen/{}'.format(category))




#############
# PLAYLISTS #   # View, Create, and Manage user playlists
#############


@login_required(login_url=reverse_lazy('login'))
def listenPlaylist(request, playlistId):
    '''
    Rendering function for a user playlist. Note this function is very similar to listen_category. 
    We use a URL variable playlistId to filter all the files in the playlist with that Id,
    then use the same template as listen_category to render that list. The template variabe 'listType' is used by the template
    to determine which actions are allowed in the category view versus playlist view, since these functions use the same template. 
    In the category view these are add to playlist and delete from library (if admin).
    In the playlist view this is instead delete from playlist. 

    Parameters:
        request (http): http GET request
        playlistId (int) : pk of the playlist in the playlist database table

    Returns:
        HttpResponseRedirect: back to the source category of the file
    '''
    userPlaylist = playlist.objects.get(id = playlistId)
    audio_objects = userPlaylist.audios.all()
    kwargs = {"activeTab":"listen", 'audio_objects':audio_objects, 'category_title':userPlaylist.name,
              'listType':'playlist', 'playlistId':userPlaylist.id}
    return render(request, "listen_files.html", kwargs)


@login_required(login_url=reverse_lazy('login'))
def createPlaylist(request):
    '''
    Handler function to create a user playlist. In the GET branch, renders
    a form used to create the playlist. In the POST branch attempts to create 
    the playlist and add the request user as the owner. If successful redirects
    to the playlist, otherwise back to the form

    Parameters:
        request (http): http GET or POST request
    
    Returns:
        HttpResponseRedirect: back to the upload url to fix errors or submit another file
    '''
    if request.method == "POST":
        form = playlist_form(request.POST)
        try:
            newPlaylist = form.save(commit=False)
            newPlaylist.owner = request.user
            newPlaylist.save()
            return HttpResponseRedirect('/listen/playlist/{}'.format(newPlaylist.id))
        except:
            pass
    return render(request, "createPlaylist.html", {"activeTab":"listen", 'form':playlist_form})


@login_required(login_url=reverse_lazy('login'))
def deletePlaylist(request, playlistId):
    '''
    Handler function to delete fa user playlist. Checks the playlist 
    exists and the request user is the playlist owner, and if so deletes the playlist. 
    Deletion of playlist cascades into the user playlist to file
    mapping model automatically from the model definition, so no need to manually
    handle that here.  

    Parameters:
        request (http): http GET request
        category (str) : URL friendly name of the category for redirection
        playlistId (int) : pk of the playlist in the playlist database table
    
    Returns:
        HttpResponseRedirect: to the home page
    '''
    userPlaylist = playlist.objects.get(id = playlistId)
    if userPlaylist.owner == request.user:
        userPlaylist.delete()
    return HttpResponseRedirect('/')


@login_required(login_url=reverse_lazy('login'))
def addToPlaylist(request, fileId, fileName):
    '''
    Handler function to add an audio_object to a playlist. In the GET branch, renders
    a form with a dropdown of the user playlists. In the POST branch, checks request 
    user owns the playlist. Then attempts to add the file to 
    the playlist and add the file object as a foreign key. If successful redirects
    to the playlist, otherwise back to the form.

    Parameters:
        request (http): http GET or POST request
        fileId (int) : pk of the audio_object in the audio_object database table
        fileName (str) : name attribute of the audio object
    
    Returns:
        HttpResponseRedirect: to the playlist if successful otherwise back to the form
    '''
    if request.method == "POST":
        form = add_to_playlist_form(request.user, request.POST)
        try:
            newPlaylistFile = form.save(commit=False)
            if newPlaylistFile.sourcePlaylist.owner == request.user:
                newPlaylistFile.file = audio_object.objects.get(id=fileId)
                newPlaylistFile.save()
                return HttpResponseRedirect('/listen/playlist/{}'.format(newPlaylistFile.sourcePlaylist.id))
            else:
                pass
        except:
            pass
    else:
        form = add_to_playlist_form(user=request.user)
    return render(request, "addToPlaylist.html", {"activeTab":"listen", 'filename':fileName, 'form':form})


@login_required(login_url=reverse_lazy('login'))
def removeFromPlaylist(request, playlistId, fileId):
    '''
    Handler function to remove an audio_object from a playlist. Checks the 
    request user is the playlist owner. If so, deletes all instances of the file
    from the playlist. In any case, redirects back to the playlist.

    Parameters:
        request (http): http GET or POST request
        playlistId (int) : pk of the playlist in the playlist database table
        fileId (int) : pk of the audio_object in the audio_object database table
    
    Returns:
        HttpResponseRedirect: to the playlist if successful otherwise back to the form
    '''
    userPlaylist = playlist.objects.get(id = playlistId)
    if userPlaylist.owner == request.user:
        file_object = audio_object.objects.get(id=fileId)
        toDel = PlaylistMapping.objects.filter(sourcePlaylist=userPlaylist, file=file_object)
        for to in toDel:
            to.delete()
    return HttpResponseRedirect('/listen/playlist/{}'.format(userPlaylist.id))




###########
# CHATBOT #
###########    


def chatbot_render(request):
    '''
    Temp standin for chatbot not yet implemented, displays we are
    working on this message.

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered chatbot template
    '''
    return render(request, "chatbot.html", {"activeTab":"chatbot"})
    