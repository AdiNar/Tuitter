from django import forms
from .models import Twit, BoxedUser
from django.contrib.auth.models import User

class TwitForm(forms.ModelForm):
    
    class Meta:
        model = Twit
        fields = ['text']
        
class FriendForm(forms.ModelForm):

    def __init__(self, current_user, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.exclude(id=current_user.id)
    
    class Meta:
        model = BoxedUser
        fields = ['user']
