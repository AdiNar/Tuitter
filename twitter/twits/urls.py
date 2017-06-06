from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add_twit/$', views.add_twit, name='add_twit'),
    url(r'^twits_list/$', views.twits_list, name="twits_list"),
]
