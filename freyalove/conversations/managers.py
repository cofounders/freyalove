from django.db import models

class ConversationManager(models.Manager):
	def fetch_conversations(self, profile):
		c_1 = super(ConversationManager, self).get_query_set().filter(owner=profile)
		c_2 = super(ConversationManager, self).get_query_set().filter(participant=profile)

		return list(c_1) + list(c_2)