from django.db import models

from freyalove.users.models import Profile, Wink
from freyalove.matchmaker.models import SexyTime, Match


NOTIFICATION_CHOICES = (
	('1', 'Wink'),
	('2', 'Match'),
	('3', 'SexyTime'),
)

STATUS_CHOICES = (
	('1', 'Accept'),
	('2', 'Not Set'),
	('3', 'Reject'),
)

class Notification(models.Model):
	# base class on which to build the rest of the notifications
	# ref: https://github.com/cofounders/freyalove/wiki/API-Objects#wiki-notification
	profile = models.ForeignKey(Profile)
	marked_for_removal = models.BooleanField(default=False)
	ntype = models.CharField(max_length=1, choices=NOTIFICATION_CHOICES)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)

	# links to triggers
	wink = models.ForeignKey(Wink, null=True)
	sexytime = models.ForeignKey(SexyTime, null=True)
	match = models.ForeignKey(Match, null=True)

	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __unicode__(self):
		return "%s -> %s (status: %s)" % (self.ntype, self.belongs_to, self.status)