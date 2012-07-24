from django.db import models

from freyalove.users.models import Profile
from freyalove.conversation.managers import ConversationManager

class Conversation(models.Model):
	owner = models.ForeignKey(Profile, related_name='owner_set')
	participant = models.ForeignKey(Profile, related_name='participant_set')
	created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = ConversationManager()

	def __unicode__(self):
		return "%s <-> %s" % (owner, participant)

class Msg(models.Model):
    conversation = models.ForeignKey(Conversation)
    message = models.TextField(blank=True)
    sender = models.ForeignKey(Profile,related_name='sender_set')
    receiver = models.ForeignKey(Profile, related_name='receiver_set')
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "%s -> %s on %s" % (sender, receiver, created_at)

