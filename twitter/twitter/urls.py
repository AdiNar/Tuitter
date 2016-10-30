"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^twits/', include('twits.urls', namespace='twits')),
    url(r'^$', views.index, name='index'),
    url(r'^log_in_user/', views.log_in_user, name='log_in_user'),
    url(r'^register_user/', views.register_user, name='register_user'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^users/', views.users, name='users'),
]
