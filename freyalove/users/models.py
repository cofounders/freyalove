from django.contrib.auth.models import User
from django.db import models

from freyalove.users.managers import FriendshipManager

import datetime

class Profile(models.Model):
    # Stuff we would infer from Facebook
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.CharField(max_length=3, blank=True)
    email = models.CharField(max_length=100, blank=True)

    # Facebook info (just whacking it all here, we can always remove later)
    fb_username = models.CharField(max_length=100, blank=True)
    fb_link = models.URLField()
    fb_id = models.CharField(max_length=100, blank=True)
    fb_profile_pic = models.URLField(blank=True)

    # Admin controls
    banned = models.BooleanField(default=False)

    # About?
    profile = models.TextField(blank=True)

    def __unicode__(self):
        return self.first_name

class Blocked(models.Model):
    belongs_to = models.ForeignKey(Profile)
    block_profile_id = models.IntegerField()

    def save(self, *args, **kwargs):
        try:
            profile_to_block = Profile.objects.get(id=self.block_profile_id)
        except Profile.DoesNotExist:
            raise ValidationError("Trying to block profile id %d for member %s but profile doesn't exist!" % (self.block_profile_id, belongs_to.first_name)) 
        super(Blocked, self).save(*args, **kwargs)

# Basic friendship 
class Friendship(models.Model):
    # taken from jtauber's django-friends
    to_profile = models.ForeignKey(Profile, related_name="friends")
    from_profile = models.ForeignKey(Profile, related_name="_unused_")
    added = models.DateField(default=datetime.datetime.today)

    objects = FriendshipManager()

    class Meta:
        unique_together = (('to_profile', 'from_profile'),)

# Activities
# Placeholders

class Wink(models.Model):
    to_profile = models.ForeignKey(Profile, related_name="wink_to")
    from_profile = models.ForeignKey(Profile, related_name="wink_from")
    received = models.BooleanField(default=False) # denotes read/received

    def __unicode__(self):
        return "wink from %s to %s" % (from_profile.first_name, to_profile.first_name)