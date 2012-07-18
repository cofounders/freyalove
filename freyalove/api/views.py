# We're only going to be using this API internally, so we can safely assume that JSON is only format required.
# That being laid on, we should try and adhere to not repeating bad stuff outlined by @jacobian 
# See: http://jacobian.org/writing/rest-worst-practices/

## imports
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

try:
	import json
except ImportError:
	import simplejson as json

import facebook

#from freyalove.matchmaker.models import MatchMaker
from freyalove.users.models import Profile, Blocked, Friendship
from freyalove.matchmaker.models import Match

from freyalove.api.utils import *


# GET
def hello(request):
	resp_data = {"hello": "api"}
	resp_json = json.JSONEncoder().encode(resp_data)
	resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
	return resp

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

	# Determine if we need to fetch the actual image object
	#cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	#if not cookie:
	#	resp = HttpResponse("Cookie not set", status=404)
	#	return resp

	#token = cookie["access_token"]

	resp_data = {}
	resp_data["id"] = profile.id
	resp_data["name"] = profile.first_name + " " + profile.last_name 
	#resp_data["photo"] = fetch_profile_picture(token)
	resp_data["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
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

	if request.method == "POST":
		return update_profile(request, profile_id)

	resp_data = {}
	resp_data["id"] = profile.id
	resp_data["first_name"] = profile.first_name
	resp_data["last_name"] = profile.last_name
	resp_data["username"] = profile.fb_username 
	resp_data["facebook_id"] = profile.fb_id
	resp_data["email"] = profile.email
	resp_data["profile"] = profile.profile
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
	return resp

def init(request):
	# parse for token in cookie
	cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	if not cookie:
		resp = HttpResponse("Cookie not set", status=404)
		return resp

	profile = is_registered_user(fetch_profile(cookie["access_token"]))

	resp_data = {}
	resp_data["id"] = profile.id
	resp_data["first_name"] = profile.first_name
	resp_data["last_name"] = profile.last_name
	resp_data["username"] = profile.fb_username 
	resp_data["facebook_id"] = profile.fb_id
	resp_data["email"] = profile.email
	resp_json = json.JSONEncoder().encode(resp_data)

	resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
	return resp

def fb_friends(request, profile_id):
	# parse for token in cookie
	cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	if not cookie:
		resp = HttpResponse("Cookie not set", status=404)
		return resp

	token = cookie["access_token"]
	friends = fetch_friends(token)

	resp_data = {}
	resp_data["friends"] = friends["data"] # we will handle the "paging" link later on when we do pagination

	resp_json = json.JSONEncoder().encode(resp_data)

	resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
	return resp

def friends_in_freya(request, profile_id):
	# parse for token in cookie
	cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	if not cookie:
		resp = HttpResponse("Cookie not set", status=404)
		return resp

	token = cookie["access_token"]
	friends = fetch_friends(token)
	friends = friends["data"]
	friends_ids = []
	for f in friends:
		friends_ids.append(f["id"])

	friends_in_freya = Profile.objects.filter(fb_id__in=friends_ids)
	resp_data = {}
	resp_data["friends"] = []

	for profile in friends_in_freya:
		resp_data["friends"].append({"name": profile.first_name + " " + profile.last_name , "id": profile.id, "photo": "http://graph.facebook.com/%s/picture" % profile.fb_username})

	resp_json = json.JSONEncoder().encode(resp_data)

	resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
	return resp

def mutual_friends_in_freya(request, profile_id, target_id):
	"""
	Given 2 ids, check that they are friends, then return a set of mutual friends in the system
	"""
	
	return HttpResponse("wip.")

def fetch_sexytimes(request):
	"""
	Returns all incoming sexytimes for a user.
	"""

	cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
	if not cookie:
		resp = HttpResponse("Cookie not set", status=404)
		return resp

	profile = is_registered_user(fetch_profile(cookie["access_token"]))
	has_match = Match.objects.has_match(profile)
	resp_data = {}
	resp_data['sexytimes'] = []

	if not has_match:
		pass
	else:
		sexytimes = Match.objects.fetch_sexytimes(profile)
		for s in sexytimes:
			s_dict = {}
			s_dict["when"] = s.when
			s_dict["where"] = s.where
			# we'll add notes when i understand the context
			resp_data['sexytimes'].append(s_dict)

	resp_json = json.JSONEncoder().encode(resp_data)

	resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
	return resp

# POST
@csrf_exempt
def update_profile(request, profile_id):
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

	if request.method == "POST":
		resp_data = {}

		profile_desc = request.POST.get("profile_desc", None)
		if not profile_desc:
			resp_data["status"] = "Fail"

		profile.profile = profile_desc
		profile.save()
		resp_data["status"] = "Success"

		resp_json = json.JSONEncoder().encode(resp_data)

		resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
		return resp
	else:
		resp = HttpResponse("Bad request", status=400)
		return resp

def create_sexytime(request):

	pass


# Direct calls to Open Graph API

def fetch_profile(token):
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	return profile

def fetch_profile_picture(token):
	graph = facebook.GraphAPI(token)
	picture = graph.get_connections("me", "picture")
	return picture

def fetch_friends(token):
	graph = facebook.GraphAPI(token)
	friends = graph.get_connections("me", "friends")
	return friends

def fetch_all_friends(token):
	graph = facebook.GraphAPI(token)
	friends = graph.get_connections("me", "friends")
	return friends

