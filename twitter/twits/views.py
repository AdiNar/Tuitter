from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Twit
from django.contrib import auth
from .forms import TwitForm
from friendship.models import Follow
from twitter.views import display_user, get_twits_for


def add_twit(request):

    form = TwitForm(request.POST)

    form.is_valid()

    twit = Twit(created_by=request.user, text=form.cleaned_data['text'])

    twit.save()

    return display_user(request, request.user.id)


def twits_list(request):
    twits = get_twits_for(request.user)
    context = {'twits': twits}
    return render(request, 'twits/twits_list.html', context)
