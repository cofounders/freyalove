# We're only going to be using this API internally, so we can safely assume that JSON is only format required.
# That being laid on, we should try and adhere to not repeating bad stuff outlined by @jacobian 
# See: http://jacobian.org/writing/rest-worst-practices/

## imports
from django.http import HttpResponse

try:
	import json
except ImportError:
	import simplejson as json

#from freyalove.matchmaker.models import MatchMaker
from freyalove.users.models import Profile, Blocked, Friendship


# READ/GET
# Returning models as resource
def matchmaker(request, matchmaker_id):
	"""
	Return information on a matchmaker given an id/fb_id
	"""
	pass

def profile(request, profile_id):
	"""
	Return information on a user profile given an id/fb_id
	"""
	try:
		profile_id = int(profile_id)
	except ValueError:
		resp = HttpResponse("Bad request", status=400)
		return resp
	try:
		profile = Profile.objects.get(id=profile_id)
	except Profile.DoesNotExist:
		try:
			profile = Profile.objects.get(fb_id=str(profile_id))
		except Profile.DoesNotExist:
			resp = HttpResponse("Not found", status=404)
			return resp

	resp_data = {}
	resp_data["first_name"] = profile.first_name
	resp_data["last_name"] = profile.last_name
	resp_data["username"] = profile.fb_username 
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = HttpResponse(resp_json, content_type="application/json")
	return resp

def are_friends(request, profile1_id, profile2_id):
	"""
	"""
	pass


# Resources that follow a template (e.g. URL)

