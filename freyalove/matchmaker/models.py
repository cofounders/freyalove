from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, pre_save, post_save

from freyalove.users.models import Profile
from freyalove.matchmaker.managers import MatchManager, SexyTimeManager, MatchProposalManager

MATCHMAKE_RESPONSES = (
    ('Pending', 'notset'),
    ('Accepted', 'accept'),
    ('Declined', 'reject'),
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
    initial_signal = models.BooleanField(default=True)

    # manager
    objects = MatchManager()

    class Meta:
        verbose_name_plural = "matches"

    def __unicode__(self):
        return "%s <-> %s by %s" % (self.p1.first_name, self.p2.first_name, self.matchmaker.first_name)

    def validate_profiles(self):
        if self.p1.banned or self.p2.banned:
            return False
        else:
            return True

    def validate_responses(self):
        valid_responses = "Pending, Accepted, Declined, Block"
        if self.p1_response not in valid_responses or self.p2_response not in valid_responses:
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        if not self.validate_profiles():
            raise ValidationError("Invalid profile in attempt to matchmake!")
        if not self.validate_responses():
            raise ValidationError("Invalid response in attempt to matchmake!")
        # mark success/reject
        if self.p1_response == "Accepted" and self.p2_response == "Accepted":
            self.success = True
            # Call method to update matchmaker score perhaps?
        elif self.p1_response == "Declined" or self.p2_response == "Declined":
            self.rejected = True
            # Call method to update matchmaker score perhaps?
        elif self.p1_response == "Block" or self.p2_response == "Block":
            # Call blocker
            pass
        else:
            pass

        super(Match, self).save(*args, **kwargs)

class MatchProposal(models.Model):
    from_profile = models.ForeignKey(Profile, related_name="from")
    to_profile = models.ForeignKey(Profile, related_name="to")
    quality = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    match = models.ForeignKey(Match, null=True)
    objects = MatchProposalManager()

class SexyTime(models.Model):
    match = models.ForeignKey(Match, null=True)
    p1 = models.ForeignKey(Profile, related_name="date1")
    p2 = models.ForeignKey(Profile, related_name="date2")
    matchmaker = models.ForeignKey(Profile, related_name="maker")

    # event fields
    where = models.CharField(max_length=300, blank=True)
    when = models.DateTimeField(null=True)
    notes = models.TextField(blank=True)

    # RSVP
    p1_attending = models.BooleanField(default=False)
    p2_attending = models.BooleanField(default=False)
    p1_responded = models.BooleanField(default=False)
    p2_responded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = SexyTimeManager()

    def __unicode__(self):
        return "%s <-> %s on %s" % (self.p1.first_name, self.p2.first_name, str(self.when))

def match_notify(sender, instance, **kwargs):
    from freyalove.notify.register import notify

    if instance.initial_signal:
        notify(instance.p1, "Match_Introduction", instance, instance.p2)
        instance.initial_signal = False
        instance.save()

post_save.connect(match_notify, sender=Match, dispatch_uid="match_save")
