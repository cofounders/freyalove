## imports
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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

# GET /USERS/:ID/PROFILE/
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

# GET /USERS/:ID/PROFILE/SUMMARY/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def profile_summary(request, fb_username):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    given_user_profile = Profile.objects.has_freya_profile_given_fb_details(fb_username)

    # TODO: Permissions check - Self, friends and friends-of-friends

    resp_data_ = obj_user_summary([given_user_profile])
    resp_data = resp_data_[0]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# GET /USERS/:ID/FRIENDS/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def friends(request, fb_username):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    given_user_profile = Profile.objects.has_freya_profile_given_fb_details(fb_username)

    # TODO: Permissions check - Self, friends

    friends = Friendship.objects.friends_for_profile(given_user_profile)

    resp_data = []
    resp_data_ = obj_user_summary([friends])

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

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
