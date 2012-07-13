# We're only going to be using this API internally, so we can safely assume that JSON is only format required.
# That being laid on, we should try and adhere to not repeating bad stuff outlined by @jacobian 
# See: http://jacobian.org/writing/rest-worst-practices/

## imports
from django.http import HttpResponse
from django.conf import settings

try:
	import json
except ImportError:
	import simplejson as json

import facebook

#from freyalove.matchmaker.models import MatchMaker
from freyalove.users.models import Profile, Blocked, Friendship


# READ/GET
# Returning models as resource
def profile_summary(request, profile_id):
	"""
	Return summarized information on a user profile given an id/fb_id
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
	resp_data["id"] = profile.id
	resp_data["name"] = profile.first_name + " " + profile.last_name 
	resp_data["photo"] = None
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = HttpResponse(resp_json, content_type="application/json")
	return resp

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
	resp_data["id"] = profile.id
	resp_data["first_name"] = profile.first_name
	resp_data["last_name"] = profile.last_name
	resp_data["username"] = profile.fb_username 
	resp_data["facebook_id"] = profile.fb_id
	resp_data["email"] = profile.email
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = HttpResponse(resp_json, content_type="application/json")
	return resp

def init(request):
	# parse for token in cookie
	cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	if not cookie:
		resp = HttpResponse("Cookie not set", status=404)
		return resp

	graph = facebook.GraphAPI(cookie["access_token"])
	profile = is_registered_user(fetch_profile(graph.get_object("me")))

	resp_data = {}
	resp_data["id"] = profile.id
	resp_data["first_name"] = profile.first_name
	resp_data["last_name"] = profile.last_name
	resp_data["username"] = profile.fb_username 
	resp_data["facebook_id"] = profile.fb_id
	resp_data["email"] = profile.email
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = HttpResponse(resp_json, content_type="application/json")
	return resp

# Resources that follow a template (e.g. URL)


# Direct calls to Open Graph API

def fetch_profile(token):
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	return profile

# Utils
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
