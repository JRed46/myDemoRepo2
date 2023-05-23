from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import login, authenticate
from .forms import register_form, login_form


def homePageRender(request):
    return render(request, 'index.html')

def log_in(request):
    '''
    View function to handle user authentication. Renders login
    form if request method is GET, otherwise if method is POST
    attempts to log in user. If credentials are invalid renders
    form with error message, otherwise redirects to home page.

    Parameters:
        request (HTTP): Http GET or POST request

    Returns:
        HttpResponseRedirect: Either to success page or error populated form
    '''
    getNext = lambda r : r.GET.get('next') if r.GET.get('next') else '/'        
    if request.user.is_authenticated:
        return HttpResponseRedirect(getNext(request)) # Redirect if user is logged in
    form = login_form(data = request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(getNext(request)) # Redirect to home page
    return render(request, 'registration/login.html', {'form': form, "activeTab":"auth"})



def create_account(request):
    '''
    View function to handle user account creation. Renders create
    form if request method is GET, otherwise if method is POST
    attempts to create an account. If credentials are invalid renders
    form with error message, otherwise creates account, authenticates 
    user, and redirects to home page.

    Parameters:
        request (HTTP): Http GET or POST request

    Returns:
        HttpResponseRedirect: Either to success page or error populated form
    '''
    if request.user.is_authenticated:
        return HttpResponseRedirect("/") # Redirect if user is logged in
    if request.method == "POST":
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = register_form()
    return render(request, "registration/register.html", {"form": form, "activeTab":"auth"})