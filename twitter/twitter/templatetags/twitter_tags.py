from django import template
from django.template import defaulttags
from django.utils.safestring import mark_safe
from friendship.models import Follow
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def link_to(link, name, arg=""):
    """Make a href to link with arg with given name.
    Link should contain {} if arg is applied.
    """
    link = link.format(arg)
    return mark_safe('<a href="{0}">{1}</a>'.format(link, name))

@register.simple_tag
def link_to_user(user, name=None):
    if name is None:
        name = user.username

    return link_to("/user/{0}".format(user.id), name)


@register.simple_tag
def get_twit_date(twit):
    return twit.get_date()

@register.simple_tag
def display_manage_friend(user, to_follow):
    template = 'twitter/manage_friend.html'

    context = {
        'user': user,
        'friend': to_follow,
        'is_following': Follow.objects.follows(user, to_follow),
    }

    return render_to_string(template, context)
