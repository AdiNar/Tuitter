"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based viewsa
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import password_change
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^twits/', include('twits.urls', namespace='twits')),
    url(r'^$', views.index, name='index'),
    url(r'^log_in_user/', views.log_in_user, name='log_in_user'),
    url(r'^register_user/', views.register_user, name='register_user'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^users/', views.users, name='users'),
    url(r'^add_friend/(?P<user_id>[0-9]+)/$', views.add_friend, name='add_friend'),
    url(r'^add_friend/$', views.add_friend, name='add_friend'),
    url(r'^remove_friend/(?P<user_id>[0-9]+)/$', views.remove_friend, name='remove_friend'),
    url(r'^passchange/$', password_change, {'template_name': 'twitter/password_change.html'}),
    url(r'^password_change_done/$', TemplateView.as_view(template_name='twitter/password_change_done.html'), name='password_change_done'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.display_user, name='display_user'),
    url(r'^user/$', views.display_user, name='display_user'),
    url(r'^statistics/(?P<user_id>[0-9]+)/$', views.statistics, name="statistics"),
    url(r'^statistics/$', views.statistics, name="statistics"),
]
