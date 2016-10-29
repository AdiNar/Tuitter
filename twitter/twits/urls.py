from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.display_user, name='display_user'),
    url(r'^add_twit/$', views.add_twit, name='add_twit'),
    url(r'^add_friend/$', views.add_friend, name='add_friend'),
]
