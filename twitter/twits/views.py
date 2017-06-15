import json

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import Twit
from django.contrib import auth
from .forms import TwitForm
from friendship.models import Follow
from twitter.views import display_user, get_twits_for
from django.core import serializers


@csrf_exempt
def add_twit(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        twit = Twit(text=text, created_by=request.user)
        twit.save()

        return render(request, 'twits/twit.html', {'twit': twit, 'display_refresh': True})
    else:
        return twits_list(request)


def twits_list(request):
    twits = get_twits_for(request.user)
    context = {'twits': twits}
    return render(request, 'twits/twits_list.html', context)
