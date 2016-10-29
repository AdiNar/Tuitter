from django.test import TestCase
 
from django.utils import timezone

from .models import Twit, Friend
from django.contrib.auth.models import User

class FriendsTest(TestCase):
    def test_is_friend_of(self):
        """ Checks if function Friend().is_friend_of works properly.

        """
        user = User(username='one')
        user.save()

        friend = User(username='two')
        friend.save()

        not_a_friend = User(username='three')
        
        friendship = Friend(user=user, friend=friend)
        friendship.save()
        
        self.assertTrue(friendship.is_friend_of(user), "Hey, don't rememer me? (users should be friends)")
        self.assertTrue(friendship.is_friend_of(friend), "Hey, don't rememer me? (users should be friends)")

        self.assertTrue(friendship.is_friend_of(not_a_friend), "Nope, those should not be friends.")

        
        
    def test_make_friends_with_yourself(self):
        """
        make_friends(User, User) should prevent making friends 
        with yourself.
        
        """
        pass

    
    def test_make_friends_simple(self):
        """
        Test default behaviour of creating friends
        """
        pass
    
