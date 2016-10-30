from .forms import LogInForm, RegisterForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from friendship.models import Follow
from twits.views import display_user
from django.views.decorators.cache import cache_control
from twits.models import Twit

RESULT_SIZE = 20

def index(request):
    context = {}
    
    if request.user.is_anonymous():
        context['log_in_form'] = LogInForm()
        context['register_form'] = RegisterForm()
        return render(request, 'twitter/index.html', context)
    else:
        context['friends_twits'] = get_twits_for(request.user)
    return render(request, 'twitter/index.html', context)

def get_twits_for(user):
    """ Returns twits created by user and friends.
    Twits are sorted by id - result is the same as sorting with created_on.
    """

    if user.is_anonymous:
        return Twit.objects.all().order_by('-created_on')[:RESULT_SIZE]
    else:
        following = Follow.objects.following(user)
        # Show twits from current user too.
        following.append(user)
        return Twit.objects.filter(created_by__in=following).order_by('-created_on')[:RESULT_SIZE]

def log_in_user(request):
    if request.method == 'POST':

        form = LogInForm(request.POST)
        if user_authenticate(request, request.POST['username'], request.POST['password']):
            return display_user_page(request)
        else:
            context = {}
            context['log_in_form'] = form
            context['register_form'] = RegisterForm()
            return render(request, 'twitter/index.html', context)
    else:
        raise Exception("log_in_user should receive post!")

# Register user, if succeeded log in and redirect to user page
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user_authenticate(request, form.cleaned_data['username'], form.cleaned_data['password1'])
            return display_user_page(request)
        else:
            context = {}
            context['log_in_form'] = LogInForm()
            context['register_form'] = form
            return render(request, 'twitter/index.html', context)
    else:
        raise Exception("register_user should reveive post!")
    
# Should always return true since form takes care of data correctness.
def user_authenticate(request, username, password):
    user = auth.authenticate(username=username, password=password)

    if user is None or user.is_anonymous:
        print("None")
        return False
    else:
        print("Auth")
        auth.login(request, user)
        return True
    
def display_user_page(request):
    return redirect('twits:display_user', user_id=request.user.id)

@cache_control(no_cache=True, must_revalidate=True)
def logout(user):
    auth.logout(user)
    return redirect('index')

def users(request):
    if request.user.is_anonymous:
        friends = []
    else:
        friends = Follow.objects.following(request.user)
    rest = User.objects.exclude(id__in=map((lambda x: x.id), friends))
                                
    context = {
        'friends': friends,
        'rest': rest,
    }
    
    return render(request, 'twitter/users.html', context)

def add_friend(request, user_id):
    to_follow = User.objects.get(id=user_id)

    Follow.objects.add_follower(request.user, to_follow)

    return display_user(request, user_id)

def remove_friend(request, user_id):
    to_follow = User.objects.get(id=user_id)

    Follow.objects.remove_follower(request.user, to_follow)

    return display_user(request, user_id)
