from django.db import models

from freyalove.users.models import Profile
from freyalove.conversations.managers import ConversationManager

class Conversation(models.Model):
    owner = models.ForeignKey(Profile, related_name='owner_set')
    participants = models.ManyToManyField(Profile, related_name='participants_set')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    unread = models.BooleanField(default=False) 
    deleted = models.BooleanField(default=False)
    
    objects = ConversationManager()

    def __unicode__(self):
        return "%s <-> %s" % (self.owner, self.participants)

class Msg(models.Model):
    conversation = models.ForeignKey(Conversation)
    message = models.TextField(blank=True)
    sender = models.ForeignKey(Profile,related_name='sender_set')
    #receiver = models.ForeignKey(Profile, related_name='receiver_set')
    read = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return "%s -> %s on %s" % (self.sender, self.conversation, self.created_at)

