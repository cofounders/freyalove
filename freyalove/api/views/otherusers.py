## imports
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

try:
    import json
except ImportError:
    import simplejson as json

import facebook

from freyalove.users.models import Profile, Blocked, Friendship, Wink, ProfileDetail, ProfilePrivacyDetail
from freyalove.matchmaker.models import Match, SexyTime
from freyalove.conversations.models import Conversation, Msg

from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import obj_user_summary, obj_user

@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def profile(request, fb_username):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    given_user_profile = Profile.objects.has_freya_profile_given_fb_details(fb_username)

    # TODO: Permissions check - Self, friends and friends-of-friends

    resp_data = []
    resp_data_ = obj_user([given_user_profile])
    resp_data["user"] = resp_data_[0]
    resp_data["pending_match"] = False # TODO 

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def profile_summary(request):
    """
    Return summarized information on a user profile given an id/fb_id
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data_ = obj_user_summary([profile])
    resp_data = resp_data_[0]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

def friends_in_freya(request, profile_id):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
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

def mutual_friends_in_freya(request, fb_username):
    """
    Given a username, check that they are friends, then return a set of mutual friends in the system
    """
    
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))
    given_user_profile = get_user(fb_username)
    resp_data = []

    if given_user_profile:
        pass

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp
