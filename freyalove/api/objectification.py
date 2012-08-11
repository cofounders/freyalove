# User
def obj_user(list_of_profiles):
	pass

# UserSummary
def obj_user_summary(list_of_profiles):
	"""
	Given a list of profiles, return a list of dictionaries with the following:
		id: String // by default use verbose userIDs (use FB username)
		firstName: String
		lastName: String
		photo: String
		points: Integer // the points on the leaderboard
	"""

	assert len(list_of_profiles) > 0, "There must be at least one profile."

	resp = []

	for profile in list_of_profiles:
		profile_as_user_summary = {}
		profile_as_user_summary["id"] = profile.fb_username
		profile_as_user_summary["firstName"] = profile.first_name
		profile_as_user_summary["lastName"] = profile.last_name
		profile_as_user_summary["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
		profile_as_user_summary["points"] = 0 # TODO
		resp.append(profile_as_user_summary)

	return resp