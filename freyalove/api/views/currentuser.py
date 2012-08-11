## imports
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
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

@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def profile_summary(request):
    """
    Return summarized information on a user profile given an id/fb_id
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = {}
    resp_data["id"] = profile.id
    resp_data["firstName"] = profile.first_name 
    resp_data["lastName"] = profile.last_name 
    resp_data["email"] = profile.email
    resp_data["fb_id"] = profile.fb_id
    resp_data["fb_link"] = profile.fb_link
    resp_data["fb_username"] = profile.fb_username
    #resp_data["photo"] = fetch_profile_picture(token)
    resp_data["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
    resp_json = json.JSONEncoder().encode(resp_data)

    resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
    return resp

@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def profile_details(request):
    """
    Return summarized information on a user profile given an id/fb_id
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = {}
    
    details_fields = ProfileDetail._meta.get_all_field_names()
    privacy_fields = ProfilePrivacyDetail._meta.get_all_field_names()
    for field in details_fields:
        resp_data[field] = getattr(profile.details, field)
    for field in privacy_fields:
        resp_data[field + "Public"] = getattr(profile.permissions, field)
    resp_json = json.JSONEncoder().encode(resp_data)

    resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
    return resp

@user_is_authenticated_with_facebook
@require_http_methods(["GET", "POST"])
def profile(request):
    """
    Return information on a user profile given an id/fb_id
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

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

@user_is_authenticated_with_facebook
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

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

@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def profile_unregister(request):
    """
    Allows the user to delete the Freya Love account. 
    A successful request to this URL deletes the account and all data stored with it. 
    The fb_id is sent only for confirmation purposes.
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = existing_user(fetch_profile(cookie["access_token"]))
    if not profile:
        resp = HttpResponse("Fail to unregister user; not registered!", status=403)
        return resp

    resp_data = {}
    fb_id = request.POST.get("fb_id", None)
    if not fb_id:
        resp_data["status"] = "Fail"
    else:
        if fb_id != profile.fb_id:
            resp_data["status"] = "Fail"
        else:
            profile.delete()
            resp_data["status"] = Success

    resp_json = json.JSONEncoder().encode(resp_data)

    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp 