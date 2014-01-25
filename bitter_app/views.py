from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from bitter_app.forms import AuthenticateForm, UserCreateForm, BeetForm
from bitter_app.models import Beet

# Create your views here.
def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        beet_form = BeetForm()
        user = request.user
        beets_self = Beet.objects.filter(user=user.id)
        beets_buddies = Beet.objects.filter(user__userprofile__in=user.profile.follows.all)
        beets = beets_self | beets_buddies
 
        return render(request,
                      'buddies.html',
                      {'beet_form': beet_form, 'user': user,
                       'beets': beets,
                       'next_url': '/', })
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()
 
        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')
def logout_view(request):
    logout(request)
    return redirect('/')
    
def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')