from .models import playlist


def get_playlists(request):
    '''
    Makes the variable userPlaylists available in all templates.

    With the design of the front end, we want users to be able to access
    all of their playlists from any page on the site. It would be 
    cumbersome to write this database query in every view function.
    This utility function addresses that issue. It is included in the
    TEMPLATES variable of audio_server/settings.py. This makes every 
    call to the Django render function additionally call this function.
    This function returns a dictionary mapping variable names to a python object,
    and the inclusion of this function name in the TEMPLATES variable
    makes the returned dictionary available to the Template we are rendering.
    It is only used in audio_server/templates/base.html, which lets users access
    all their playlists from the topnav under "Listen" on every page of the site.

    Parmeters:
        request (http): http GET request

    Returns:
        Dict : mapping strings of template variable names to a python object.
                These objects become available to all templates.
    
    '''
    # Get user playlists of the user is authenticated
    if request.user.is_authenticated:
        return {'userPlaylists': playlist.objects.filter(owner=request.user)} 
    # Return an empty list if they are not authenticated
    return {'userPlaylists': []}


def get_adminUser(request):
    '''
    Makes the variable adminUser available in all templates.
    Very similar to get_playlists but for whether the user 
    is an admin.    

    Parmeters:
        request (http): http GET request

    Returns:
        Dict : mapping strings of template variable names to a python object.
                These objects become available to all templates.
    
    '''
    # Get user playlists of the user is authenticated
    if request.user.is_authenticated:
        return {'adminUser': is_admin(request.user)} 
    # Return an empty list if they are not authenticated
    return {'adminUser': False}



def is_admin(user):
    '''
    Checks if a user has admin privledges.

    In this application, we use membership in a Django group called "Admin"
    to determine whether a user has admin privledges. Note this does not give 
    users access to the Django admin interface, rather gives them CRUD permissions
    on our custom front end. This is called by functionalitites like delete file 
    from library before we allow the operation. Users should be added to the "Admin"
    group by the site superuser throught the Django admin interface. Also Note
    the "Admin" group will need to be created when starting a new implementation of the site. 

    Parameters:
        user (User) : Django User object

    Returns:
        Bool : Whether the user is in the admin group 
    '''
    return user.groups.filter(name='Admin').exists()




############
# MAPPINGS #
############


# Used to display the entire audio library by category
# The URL /listen/{{category}} should display the entire library with {{category}}
# Maps the {{category}} used by the front end URL to the category name in the database
categoryToAbreviation = {'nature-sounds':'NS', 'binaural-beats':'BB', 
                        'breathing-excercises':'BE', 'stories':'S', 
                        'guided-mediations':'GM', 'indian-ragas':'IR',
                        'mediation-music':'MM', 'short-guided-mediations':'SGM', 
                        'vocal-chanting':'VC'}


# Used to display a page title for a category, similar to categoryToAbreviation
# Maps the {{category}} used by the front end URL to a page title
categoryToTitle = {'nature-sounds':'Nature Sounds', 'binaural-beats':'Binaural Beats', 
                'breathing-excercises':'Breathing Excercises', 'stories':'Stories', 
                'guided-mediations':'Guided Meditations', 'indian-ragas':'Indian Ragas',
                'mediation-music':'Meditation Music', 'short-guided-mediations':'Short Guided Meditations', 
                'vocal-chanting':'Vocal Chanting'}


# Inverse of categoryToAbreviation
abreviationToCategory = {'NS':'nature-sounds', 'BB':'binaural-beats', 
                        'BE':'breathing-excercises', 'S':'stories', 
                        'GM':'guided-mediations', 'IR':'indian-ragas',
                        'MM':'mediation-music', 'SGM':'short-guided-mediations', 
                        'VC':'vocal-chanting'}