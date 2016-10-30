from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Email activation is not supported.
class LogInForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass
       

class RegisterForm(UserCreationForm):
    pass
