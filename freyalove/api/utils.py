from freyalove.users.models import Profile, Blocked, Friendship
from freyalove.matchmaker.models import Match

import datetime

# Utils
def inject_cors(resp_obj):
	resp_obj['Access-Control-Allow-Origin'] = '*'
	resp_obj['Access-Control-Allow-Headers'] = 'Authorization'

	# usually used in preflight, but we just give it all the time
	resp_obj['Access-Control-Allow-Methods'] = 'GET,POST,PUT'
	resp_obj['Access-Control-Allow-Credentials'] = 'true'

	return resp_obj

def is_registered_user(profile_dict):
	"""
	Checks if a user is already registered with us, if not, we register him
	"""
	if profile_dict:
		fb_id = profile_dict["id"]
		try:
			profile = Profile.objects.get(fb_id=fb_id)
			return profile
		except Profile.DoesNotExist:
			profile = create_freya_profile(profile_dict)
			return profile

def create_freya_profile(profile_dict):
	profile = Profile()
	profile.first_name = profile_dict["first_name"]
	profile.last_name = profile_dict["last_name"]
	profile.fb_id = profile_dict["id"]
	profile.fb_username = profile_dict["username"]
	profile.fb_link = profile_dict["link"]
	profile.email = profile_dict["email"]
	profile.save()
	return profile

def convert_to_dtobj(txt_date):
	return datetime.datetime.now()