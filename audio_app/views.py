from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import audio_object_form
from .models import audio_object




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

    audio_objects = audio_object.objects.filter(category = categoryToAbreviation.get(category))
    objs = audio_object.objects.all()
    for o in objs:
        print(o.category)
    return render(request, "listen_category.html", {"activeTab":"listen", 'audio_objects':audio_objects})


def file_upload(request):
    '''
    TODO: admin authenticate
    '''
    categories = audio_object.CHOICES
    if request.method == "POST":
        form = audio_object_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, "upload.html", {'categories': categories, "activeTab":"upload", 'form':audio_object_form})


def file_delete(request, file_id):
    '''
    TODO: admin authenticate, confirm on front end
    '''
    file_to_delete = audio_object.objects.get(id = file_id)
    if file_to_delete:
        file_to_delete.delete()
    return HttpResponseRedirect('/listen/')
    