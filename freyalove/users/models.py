from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save, post_save

from freyalove.users.managers import FriendshipManager, WinkManager

import datetime

class ProfilePrivacyDetail(models.Model):
    last_name = models.BooleanField(default=False)
    photo = models.BooleanField(default=False)
    date_of_birth = models.BooleanField(default=False)
    about = models.TextField(default=False)
    points = models.IntegerField(default=False)
    location = models.BooleanField(default=False)
    origin = models.BooleanField(default=False)
    languages = models.BooleanField(default=False)
    likes = models.BooleanField(default=False)
    likes_activities = models.BooleanField(default=False)
    likes_athletes = models.BooleanField(default=False)
    likes_books = models.BooleanField(default=False)
    likes_games = models.BooleanField(default=False)
    likes_people = models.BooleanField(default=False)
    likes_interests = models.BooleanField(default=False)
    likes_movies = models.BooleanField(default=False)
    likes_sportsteams = models.BooleanField(default=False)
    likes_sports = models.BooleanField(default=False)
    likes_tv = models.BooleanField(default=False)
    likes_quotes = models.BooleanField(default=False)

class ProfileDetail(models.Model):
    # holds the details of a user
    # ref: https://github.com/cofounders/freyalove/wiki/API-Objects#wiki-userprivacydetail
    date_of_birth = models.CharField(max_length=10, blank=True)
    about = models.TextField(blank=True)
    points = models.IntegerField(max_length=3, null=True)
    location = models.CharField(max_length=50, blank=True)
    origin = models.CharField(max_length=50, blank=True)
    languages = models.CharField(max_length=200, blank=True)
    likes = models.CharField(max_length=300, blank=True)
    likes_activities = models.CharField(max_length=300, blank=True)
    likes_athletes = models.CharField(max_length=300, blank=True)
    likes_books = models.CharField(max_length=300, blank=True)
    likes_games = models.CharField(max_length=300, blank=True)
    likes_people = models.CharField(max_length=300, blank=True)
    likes_interests = models.CharField(max_length=300, blank=True)
    likes_movies = models.CharField(max_length=300, blank=True)
    likes_sportsteams = models.CharField(max_length=300, blank=True)
    likes_sports = models.CharField(max_length=300, blank=True)
    likes_tv = models.CharField(max_length=300, blank=True)
    likes_quotes = models.CharField(max_length=300, blank=True)

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

    # extra
    details = models.ForeignKey(ProfileDetail, null=True)
    permissions = models.ForeignKey(ProfilePrivacyDetail, null=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        if not self.details:
            details = ProfileDetail()
            details.save()
            self.details = details
        if not self.permissions:
            permissions = ProfilePrivacyDetail()
            permissions.save()
            self.permissions = permissions

        super(Profile, self).save(*args, **kwargs)

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
    accepted = models.BooleanField(default=False)

    objects = WinkManager()

    def __unicode__(self):
        return "wink from %s to %s" % (from_profile.first_name, to_profile.first_name)

def register_wink(sender, instance, **kwargs):
    from freyalove.notifications.models import Notification
    try:
        n = Notification.objects.get(wink=instance)
        if instance.accepted and instance.received:
            n.status = "1"
            n.marked_for_removal = True
        elif instance.received and not instance.accepted:
            n.status = "2"
            n.marked_for_removal = True
        else:
            pass
        n.save()
    except Notification.DoesNotExist:
        n = Notification()
        n.profile = instance.to_profile
        n.ntype = "1"
        n.status = "2"
        n.wink = instance
        n.save()

# Register with freyalove.notifications
post_save.connect(register_wink, sender=Wink, dispatch_uid="wink_save")
