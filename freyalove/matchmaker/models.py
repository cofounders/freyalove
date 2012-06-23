from django.core.exceptions import ValidationError
from django.db import models

from freyalove.users.models import Profile

MATCHMAKE_RESPONSES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Declined', 'Declined'),
    ('Block', 'Block'),
)

class Match(models.Model):
    # the people
    matchmaker = models.ForeignKey(Profile, related_name="matchmaker")
    p1 = models.ForeignKey(Profile, related_name="prospect1")
    p2 = models.ForeignKey(Profile, related_name="prospect2")

    # state/switches
    success = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    p1_response = models.CharField(choices=MATCHMAKE_RESPONSES, default="Pending", max_length=10)
    p2_response = models.CharField(choices=MATCHMAKE_RESPONSES, default="Pending", max_length=10)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "%s <-> %s by %s" % (p1.first_name, p2.first_name, matchmaker.first_name)

    def save(self, *args, **kwargs):
        # mark success/reject
        if self.p1_response == "Accepted" and self.p2_response == "Accepted":
            self.success = True
            # Call method to update matchmaker score perhaps?
        elif self.p1_response == "Declined" and self.p2_response == "Declined":
            self.rejected = True
            # Call method to update matchmaker score perhaps?
        elif self.p1_response == "Block" and self.p2_response == "Block":
            # Call blocker
            pass
        else:
            pass

        super(Match, self).save(*args, **kwargs)

#class MatchMaker(models.Model):
#    matchmaker = models.ForeignKey(Profile)
#
#    def __unicode__(self):
#        return self.matchmaker.first_name