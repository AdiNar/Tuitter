from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Twit, Friend
from django.contrib import auth
from .forms import TwitForm, FriendForm

def index(request):
    return HttpResponse("Hello")

def display_user(request, user_id, error_context={}):
    """Display page for given user, contains forms to add friends and twits.

    error_context should contain form with errors if any occur.
    """ 
    user = User.objects.get(id=user_id)
    friends = Friend.objects.filter(user=user_id)
    twits = Twit.objects.filter(created_by=user).order_by('-created_on')[:10]
    logged_user_id = request.user.id
    add_twit_form = TwitForm()
    add_friend_form = FriendForm(request.user)

    context = {
        'user_twits': twits,
        'user': user,
        'friends': friends,
        'logged_user_id': logged_user_id,
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
        print("Valid")
        from_form = form.save(commit=False)
        from_form.user = current_user
        
        print(from_form)
        from_form.save()
     
    else:
        print("Invalid")
   
    return display_user(request, request.user.id, {'add_friend_form':form})
