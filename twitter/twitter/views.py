from .forms import LogInForm, RegisterForm, FriendForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from friendship.models import Follow
from django.views.decorators.cache import cache_control
from twits.models import Twit
from twits.forms import TwitForm

# Maximum number of displayed twits
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

def display_user(request, user_id=-1, error_context={}):
    """Display page for given user, contains forms to add friends and twits.

    error_context should contain form with errors if any occur.
    """
    # No user specified, show page for current.
    if user_id == -1:
        user_id = request.user.id
        
    user = User.objects.get(id=user_id)
    friends = Follow.objects.following(user=user)
    twits = Twit.objects.filter(created_by=user).order_by('-created_on')[:RESULT_SIZE]
    logged_user = request.user
    add_twit_form = TwitForm()
    add_friend_form = FriendForm(request.user)

    context = {
        'user_twits': twits,
        'user': user,
        'friends': friends,
        'logged_user': logged_user,
        'add_twit_form': add_twit_form,
        'add_friend_form': add_friend_form,
    }

    print(context)
    
    return render(request, 'twitter/display_user.html', context)


def get_twits_for(user):
    """ Returns twits created by user and his friends.
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


def register_user(request):
    """ Register user, if succeeded log in and redirect to user page.
    """
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
    return redirect('display_user', user_id=request.user.id)

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

def add_friend(request, user_id=-1):
    """ Add friend from form (POST) or by link.
    When using form user_id is not provided, -1 means no id.
    
    """
    if request.method == 'POST':
        current_user = auth.get_user(request)
        form = FriendForm(current_user, data=request.POST)

        if form.is_valid():
            to_follow = form.save(commit=False)
            Follow.objects.add_follower(request.user, to_follow.user) 
            return display_user(request, request.user.id, {'add_friend_form':form})
        else:
            raise Exception("Add friend form invalid, this should not happen")
    else:
        to_follow = User.objects.get(id=user_id)
        Follow.objects.add_follower(request.user, to_follow)
        return display_user(request, user_id)

def remove_friend(request, user_id):
    to_follow = User.objects.get(id=user_id)

    Follow.objects.remove_follower(request.user, to_follow)

    return display_user(request, user_id)

