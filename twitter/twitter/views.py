# coding=utf-8
from django.db.models import F, Min, DurationField
from django.db.models.aggregates import Count
from django.db.models.expressions import Subquery, OuterRef, Case, When, ExpressionWrapper
from django.db.models.functions import Length
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import LogInForm, RegisterForm, FriendForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from friendship.models import Follow, Friend
from django.views.decorators.cache import cache_control
from twits.models import Twit
from twits.forms import TwitForm
from templatetags.twitter_tags import link_to_user

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
    twits = get_twits_for(user=user)
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
        twits = Twit.objects.filter(created_by__in=following)\
            .order_by('-created_on')[:RESULT_SIZE]

        # subquery to take twits created after given.
        query = Twit.objects.filter(created_on__gt=OuterRef('created_on'))

        # Adds time in seconds showing how many seconds passed since last twit.
        return twits\
            .annotate(next=
                Min(
                    Subquery(query.values('created_on'))
                )
            )\
            .annotate(time_to_next_twit=
                Case(
                    When(next__isnull=True, then=None),
                    default=ExpressionWrapper(F('next') - F('created_on'),
                                              output_field=DurationField())
                )
            )


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


@csrf_exempt
def add_friend(request, user_id=-1):
    """ Add friend from form (POST) or by link.
    When using form user_id is not provided, -1 means no id.
    """
    if request.method == 'POST':
        to_follow = User.objects.get(id=user_id)
        Follow.objects.add_follower(request.user, to_follow)
        return HttpResponse(link_to_user(to_follow) + "<br>")
    else:
        to_follow = User.objects.get(id=user_id)
        Follow.objects.add_follower(request.user, to_follow)
        return display_user(request, user_id)


def remove_friend(request, user_id):
    to_follow = User.objects.get(id=user_id)

    Follow.objects.remove_follower(request.user, to_follow)

    return display_user(request, user_id)


def get_length_distribution(user):
    objects = Twit.objects\
        .filter(created_by__in=Follow.objects.following(user))\
        .annotate(twit_len=Length('text'), user=F('created_by__username'))\
        .values('user', 'twit_len')\
        .annotate(count=Count('twit_len'))\
        .order_by('user', 'twit_len')

    return objects


def get_friends_friends(user):
    followers = Follow.objects\
        .filter(follower=user).values('followee')

    return Follow.objects\
        .filter(follower__in=followers)\
        .exclude(followee__in=followers)





def statistics(request, user_id=-1):
    context = {}

    context['length_dist'] = get_length_distribution(request.user)
    context['friends_friends'] = get_friends_friends(request.user)

    return render(request, 'twitter/stats.html', context)