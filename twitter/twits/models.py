from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.defaultfilters import date
from datetime import datetime, timedelta
from django.utils import timezone


class Twit(models.Model):
    text = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(editable=False, auto_now_add=True)
    text_length = models.IntegerField(default=0)
    
    def __str__(self):
        return 'Twit: "{0}" created by {1} on {2}'.format(
            self.text, self.created_by, self.get_date())

    def save(self, *args, **kwargs):
        self.text_length = len(self.text)
        super(Twit, self).save(*args, **kwargs)

    # Returns nice looking date of creation. For shorter
    # periods returns hour, day of week,
    # for longer - year and month etc.
    def get_date(self):
        result_format = str()
        now_timezone_aware = timezone.make_aware(datetime.now())
        time_passed = now_timezone_aware - self.created_on
        
        if time_passed > timedelta(weeks=1):
            result_format += 'j b'
            
        else:
            if time_passed > timedelta(days=1):
                result_format += 'l '
            result_format += 'G:i'

        return date(self.created_on, result_format)
