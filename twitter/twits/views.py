from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Twit
from django.contrib import auth
from .forms import TwitForm, FriendForm
from friendship.models import Follow

def index(request):
    return HttpResponse("Hello")

def display_user(request, user_id=-1, error_context={}):
    """Display page for given user, contains forms to add friends and twits.

    error_context should contain form with errors if any occur.
    """
    # No user specified, show page for current
    if user_id == -1:
        user_id = request.user.id
        
    user = User.objects.get(id=user_id)
    friends = Follow.objects.following(user=user)
    twits = Twit.objects.filter(created_by=user).order_by('-created_on')[:10]
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
    }#.update(error_context)

    print(context)
    
    return render(request, 'twits/display_user.html', context)

def add_twit(request):

    form = TwitForm(request.POST)

    form.is_valid()
    
    twit = Twit(created_by=request.user, text=form.cleaned_data['text'])
    
    twit.save()

    return display_user(request, request.user.id)

def add_friend(request):
    current_user = auth.get_user(request)
    form = FriendForm(current_user, data=request.POST)
    
    if form.is_valid():
        to_follow = form.save(commit=False)
        Follow.objects.add_follower(request.user, to_follow.user) 
     
    else:
        print("Invalid")
   
    return display_user(request, request.user.id, {'add_friend_form':form})
