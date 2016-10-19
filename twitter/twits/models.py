from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 

class Twit(models.Model):
    text = models.CharField(max_length=100)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    createdOn = models.DateTimeField(editable=False)
