from django.db import models

class ConversationManager(models.Manager):
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
		