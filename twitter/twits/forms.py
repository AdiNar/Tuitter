from django import forms
from .models import Twit, Friend
from django.contrib.auth.models import User

class TwitForm(forms.ModelForm):
    
    class Meta:
        model = Twit
        fields = ['text']

class FriendForm(forms.ModelForm):

    def __init__(self, current_user, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)
        
        try:
            self.fields['friend'].queryset = User.objects.exclude(id=current_user.id) 
        except AttributeError:
            # Queryset should only be set when form is displaying.
            print("ERROR")
            pass 
    
    class Meta:
        model = Friend
        fields = ['friend']
