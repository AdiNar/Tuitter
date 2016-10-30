from .forms import LogInForm, RegisterForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

def index(request):
    context = {}
    
    if request.user.is_anonymous():
        context['log_in_form'] = LogInForm()
        context['register_form'] = RegisterForm()
        return render(request, 'twitter/index.html', context)
    else:
        context['friends_twits'] = get_twits_for(request.user)
    return render(request, 'twitter/index.html', context)

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

def logout(user):
    auth.logout(user)
    return redirect('index')

