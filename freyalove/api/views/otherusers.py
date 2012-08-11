## imports
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

try:
    import json
except ImportError:
    import simplejson as json

import facebook

from freyalove.users.models import Profile, Blocked, Friendship, Wink, ProfileDetail, ProfilePrivacyDetail
from freyalove.matchmaker.models import Match, SexyTime
from freyalove.conversations.models import Conversation, Msg

from freyalove.api.utils import *
from freyalove.api.objectification import user_summary

def get_user_summary(request, fb_username):
    """
    Return summarized information on a user profile given an fb_username
    """
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    given_user_profile = get_user(fb_username)
    resp_data = {}

    if given_user_profile:
        resp_data_ = user_summary([given_user_profile])
        if len(resp_data_) > 0:
            resp_data = resp_data_[0]

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
    return resp


def fb_friends(request, profile_id):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
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

def search(request):
    query = request.GET.get('q', None)
    resp_data = []

    if not query:
        pass
    else:
        profiles = Profile.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        resp_data = user_summary(profiles)

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp 
