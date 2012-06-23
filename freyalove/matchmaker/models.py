from django.db import models

from freyalove.users.models import Profile

class Match(models.Model):
    # the people
    matchmaker = models.ForeignKey(Profile, related_name="matchmaker")
    p1 = models.ForeignKey(Profile, related_name="prospect1")
    p2 = models.ForeignKey(Profile, related_name="prospect2")

    # state/switches
    success = models.BooleanField(default=False)
    p1_accept = models.BooleanField(default=False)
    p2_accept = models.BooleanField(default=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "%s <-> %s by %s" % (p1.first_name, p2.first_name, matchmaker.first_name)