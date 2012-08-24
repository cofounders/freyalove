from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from freyalove.users.models import Profile

# A simplier model/app derived from Actor, Verb, Target, Instance idea

class Note(models.Model):
	belongs_to = models.ForeignKey(Profile, related_name="belongs") # a note must belong to a profile
	actor = models.ForeignKey(Profile, null=True, related_name="actor") # an actor is another profile in the system that has triggered this note
	verb = models.CharField(max_length=300) # see parser for more details
	unread = models.BooleanField(default=True) # state for determining if a note has been read or not 

	# generic magic
	content_type = models.ForeignKey(ContentType, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	def __unicode__(self):
		return "note for %s: %s" % (self.belongs_to, self.verb)
	