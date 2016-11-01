from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import BoxedUser
from django import forms
from django.contrib.auth.models import User

# Email activation is not supported.
class LogInForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
       

class RegisterForm(UserCreationForm):
    pass

class FriendForm(forms.ModelForm):

    def __init__(self, current_user, *args, **kwargs):
        super(FriendForm, self).__init__(*args, **kwargs)

        self.fields['user'].queryset = User.objects.exclude(id=current_user.id)
    
    class Meta:
        model = BoxedUser
        fields = ['user']
