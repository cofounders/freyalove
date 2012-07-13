from django.db import models

from freyalove.users.models import Profile

class Message(models.Model):
    # should we bundle the messages to a conversation?
    message = models.TextField(blank=True)
    sender = models.ForeignKey(Profile,related_name='sender_set')
    receiver = models.ForeignKey(Profile, related_name='receiver_set')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "%s -> %s on %s" % (sender, receiver, created_at)

