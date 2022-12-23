from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import audio_object_form, playlist_form, add_to_playlist_form
from .models import audio_object, audioCategories, playlist, PlaylistMapping


def get_playlists(request):
    '''
    See the templates variable in settings.
    Makes the variable userPlaylists available in all templates
    '''
    if request.user.is_authenticated:
        return {'userPlaylists': playlist.objects.filter(owner=request.user)} 
    return {'userPlaylists': []}

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


####################
# HOME PAGES VIEWS #
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


def chatbot_render(request):
    '''
    Temp standin for chatbot not yet implemented

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered chatbot template
    '''
    return render(request, "home/chatbot.html", {"activeTab":"chatbot"})


################
# LISTEN VIEWS #
################    


def listen(request):
    '''
    Rendering function for the listen landing page. This is the page that users are 
    shown when they click "listen" in the topnav. Shows the 9 categories and lets users 
    click into the categories. Users do not need authentication for this page but do for the sublists.
    Corresponding url is '/listen'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered instructions template
    '''
    return render(request, "listen_categories.html", {"activeTab":"listen"})


@login_required(login_url=reverse_lazy('login'))
def listen_category(request, category):
    '''
    Rendering function for the listen landing page. This is the page that users are 
    shown when they click "listen" in the topnav. Shows the 9 categories and lets users 
    click into the categories. Users do not need authentication for this page but do for the sublists.
    Corresponding url is '/listen'

    Parameters:
        request (http): http GET request
    
    Returns:
        HttpResponseRedirect: the rendered instructions template
    '''
    audio_objects = []
    categoryToAbreviation = {'nature-sounds':'NS', 'binural-beats':'BB', 
                            'breathing-excercises':'BE', 'stories':'S', 
                            'guided-mediations':'GM', 'indian-ragas':'IR',
                            'mediation-music':'MM', 'short-guided-mediations':'SGM', 
                            'vocal-chanting':'VC'}

    categoryToTitle = {'nature-sounds':'Nature Sounds', 'binural-beats':'Binural Beats', 
                    'breathing-excercises':'Breathing Excercises', 'stories':'Stories', 
                    'guided-mediations':'Guided Meditations', 'indian-ragas':'Indian Ragas',
                    'mediation-music':'Meditation Music', 'short-guided-mediations':'Short Guided Meditations', 
                    'vocal-chanting':'Vocal Chanting'}

    audio_objects = audio_object.objects.filter(category = categoryToAbreviation.get(category))
    adminUser = is_admin(request.user)
    kwargs = {"activeTab":"listen", 'audio_objects':audio_objects, 'category_title':categoryToTitle.get(category),
              'listType':'category', 'adminUser':adminUser}
    return render(request, "listen_files.html", kwargs)



@login_required(login_url=reverse_lazy('login'))
def listenPlaylist(request, playlistId):
    userPlaylist = playlist.objects.get(id = playlistId)
    audio_objects = userPlaylist.audios.all()
    kwargs = {"activeTab":"listen", 'audio_objects':audio_objects, 'category_title':userPlaylist.name,
              'listType':'playlist', 'playlistId':userPlaylist.id}
    return render(request, "listen_files.html", kwargs)


@login_required(login_url=reverse_lazy('login'))
def createPlaylist(request):
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
    userPlaylist = playlist.objects.get(id = playlistId)
    if userPlaylist.owner == request.user:
        userPlaylist.delete()
    return HttpResponseRedirect('/')


@login_required(login_url=reverse_lazy('login'))
def addToPlaylist(request, fileId, fileName):
    if request.method == "POST":
        form = add_to_playlist_form(request.user, request.POST)
        try:
            newPlaylistFile = form.save(commit=False)
            newPlaylistFile.file = audio_object.objects.get(id=fileId)
            newPlaylistFile.save()
            return HttpResponseRedirect('/listen/playlist/{}'.format(newPlaylistFile.sourcePlaylist.id))
        except:
            pass
    else:
        form = add_to_playlist_form(user=request.user)
    return render(request, "addToPlaylist.html", {"activeTab":"listen", 'form':form})


@login_required(login_url=reverse_lazy('login'))
def removeFromPlaylist(request, playlistId, fileId):
    userPlaylist = playlist.objects.get(id = playlistId)
    if userPlaylist.owner == request.user:
        file_object = audio_object.objects.get(id=fileId)
        toDel = PlaylistMapping.objects.filter(sourcePlaylist=userPlaylist, file=file_object)
        for to in toDel:
            to.delete()
    return HttpResponseRedirect('/listen/playlist/{}'.format(userPlaylist.id))



#ADMIN 
@login_required(login_url=reverse_lazy('login'))
def file_upload(request):
    '''
    TODO: admin authenticate
    '''
    if request.method == "POST":
        form = audio_object_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, "upload.html", {"activeTab":"upload", 'form':audio_object_form})


@login_required(login_url=reverse_lazy('login'))
def file_delete(request, file_id):
    '''
    TODO: admin authenticate, confirm on front end
    '''
    if is_admin(request.user):
        file_to_delete = audio_object.objects.get(id = file_id)
        if file_to_delete:
            file_to_delete.delete()
    return HttpResponseRedirect('/listen/')
    