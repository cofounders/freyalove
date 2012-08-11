from freyalove.users.models import Profile, Wink
# ref: https://github.com/cofounders/freyalove/wiki/Algorithm-Match-Fit

def match_fit(profile_1, profile_2):
	"""
	Calculates a score (0 - 100) based on questions answered by 2 profiles.
	"""

	score = 0

	# A mutual wink adds 20%
	if Wink.objects.has_wink(profile_1, profile_2):
		if score <= 80:
			score += 20
		else:
			score = 100
	return score
