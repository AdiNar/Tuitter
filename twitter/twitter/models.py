from django.db import models
from django.contrib.auth.models import User

class BoxedUser(models.Model):
    """ Used only to display ModelChoiceField with users
    """
    user = models.ForeignKey(User)
