from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import Http404
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
        beets = beets.order_by('id').reverse()
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

@login_required
def submit(request):
    if request.method == "POST":
        beet_form = BeetForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if beet_form.is_valid():
            beet = beet_form.save(commit=False)
            beet.user = request.user
            beet.save()
            return redirect(next_url)
        else:
            return public(request, beet_form)
    return redirect('/')

@login_required
def public(request, beet_form=None):
    beet_form = beet_form or BeetForm()
    beets = Beet.objects.order_by('id').reverse()[:10]
    return render(request,
                  'public.html',
                  {'beet_form': beet_form, 'next_url': '/beets',
                   'beets': beets, 'username': request.user.username})

def get_latest(user):
    try:
        return user.beet_set.order_by('-id')[0]
    except IndexError:
        return ""
        
@login_required
def users(request, username="", beet_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        beets = Beet.objects.filter(user=user.id).order_by('id').reverse()
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile or buddies' profile
            return render(request, 'user.html', {'user': user, 'beets': beets, })
        return render(request, 'user.html', {'user': user, 'beets': beets, 'follow': True, })
    users = User.objects.all().annotate(beet_count=Count('beet'))
    beets = map(get_latest, users)
    obj = zip(users, beets)
    beet_form = beet_form or BeetForm()
    return render(request,
                  'profiles.html',
                  {'obj': obj, 'next_url': '/users/',
                   'beet_form': beet_form,
                   'username': request.user.username, })
 
@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')
