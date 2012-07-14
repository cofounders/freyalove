from django.db import models

import datetime

class MatchManager(models.Manager):
	def has_match(self, profile):
		matches = super(MatchManager, self).get_query_set().filter(p1=profile)
		if matches.count() == 0:
			matches = super(MatchManager, self).get_query_set().filter(p2=profile)
			if matches.count() == 0:
				return False
			else:
				return True
		else:
			return True

	def all_matches(self, profile):
		matches_1 = list(super(MatchManager, self).get_query_set().filter(p1=profile))
		matches_2 = list(super(MatchManager, self).get_query_set().filter(p2=profile))

		return matches_1 + matches_2

	def fetch_sexytimes(self, profile):
		now = datetime.datetime.now()
		sexytimes_1 = super(MatchManager, self).get_query_set().filter(p1=profile, when__gte=now)
		sexytimes_2 = super(MatchManager, self).get_query_set().filter(p2=profile, when__gte=now)

		return sexytimes_1 + sexytimes_2