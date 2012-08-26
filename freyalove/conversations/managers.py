from django.db import models

class ConversationManager(models.Manager):
    def has_conversation(self, profiles):
        has_conversation = False
        conversations = super(ConversationManager, self).get_query_set().filter(participants__in=profiles)
        for c in conversations:
            c_profiles = set(list(c.participants.all()))
            if c_profiles == set(profiles):
                has_conversation = True
        return has_conversation

    def get_conversations(self, profiles):
        conversations = super(ConversationManager, self).get_query_set().filter(participants__in=profiles)
        for c in conversations:
            c_profiles = set(list(c.participants.all()))
            if c_profiles == set(profiles):
                return c
        return None

    # old methods assuming 1-1 conversations
    def fetch_conversations(self, profile):
        c_1 = super(ConversationManager, self).get_query_set().filter(owner=profile)
        c_2 = super(ConversationManager, self).get_query_set().filter(participant=profile)

        return list(c_1) + list(c_2)

    def fetch_unread_conversations(self, profile):
        c_1 = super(ConversationManager, self).get_query_set().filter(owner=profile, unread=True)
        c_2 = super(ConversationManager, self).get_query_set().filter(participant=profile, unread=True)

        return list(c_1) + list(c_2)

    def delete_conversation(self, conversation_id):
        try:
            c = super(ConversationManager, self).get_query_set().get(id=conversation_id)
        except self.model.DoesNotExist:
            c = None

        if c:
            c.deleted = True
            c.save()
            # mark all messages
            msgs = c.msg_set.all()
            for m in msgs:
                m.deleted = True
                m.save()
        