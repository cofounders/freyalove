from django.contrib.auth.models import User
from django.db import models

from freyalove.users.managers import FriendshipManager

import datetime

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.CharField(max_length=3, blank=True)

    # Facebook info (just whacking it all here, we can always remove later)
    fb_username = models.CharField(max_length=100, blank=True)
    fb_link = models.URLField()
    fb_id = models.CharField(max_length=100, blank=True)
    fb_profile_pic = models.URLField(blank=True)

    def __unicode__(self):
        return self.first_name

# Basic friendship 
class Friendship(models.Model):
    # taken from jtauber's django-friends
    to_profile = models.ForeignKey(Profile, related_name="friends")
    from_profile = models.ForeignKey(Profile, related_name="_unused_")
    added = models.DateField(default=datetime.datetime.today)

    objects = FriendshipManager()

    class Meta:
        unique_together = (('to_profile', 'from_profile'),)

# Matchmaking