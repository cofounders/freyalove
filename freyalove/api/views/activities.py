## imports
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q

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
from freyalove.api.objectification import obj_user_summary, obj_user, obj_fb_user_summary, obj_wink, obj_sexytimes


# GET /ACTIVITIES/SEXYTIMES/UPCOMING/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def fetch_sexytimes(request):
    """
    Returns all incoming sexytimes for a user.
    """

    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    sexytimes = SexyTime.objects.fetch_sexytimes(profile)

    resp_data = obj_sexytimes(sexytimes)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# GET /ACTIVITIES/WINKS/UNRETURNED/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def fetch_winks(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    winks = Wink.objects.filter(to_profile=profile, accepted=False, hide=False)

    resp_data = obj_wink(winks)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# GET /ACTIVITIES/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def fetch_activities(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    winks = Wink.objects.filter(to_profile=profile)
    sexytimes = SexyTime.objects.fetch_sexytimes(profile)

    resp_data = []

    winks_as_objects = obj_wink(winks)
    sexytimes_as_objects = obj_sexytimes(sexytimes)

    resp_data = [winks_as_objects + sexytimes_as_objects]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# POST /ACTIVITIES/SEXYTIMES/CREATE/
@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def create_sexytime(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    p2 = request.POST.get("to", None)
    when = request.POST.get("when", None)
    where = request.POST.get("where", None)
    resp_data = {}

    if p2:
        p2 = Profile.objects.has_freya_profile_given_fb_details(p2)

    if p2 and when and where:
        # parse date
        when_parsed = convert_to_dtobj(when)

        sexytime = SexyTime()
        sexytime.p1 = profile
        sexytime.p1_response = "accept" # by default, creator accepts event
        sexytime.p2 = p2
        sexytime.when = when_parsed
        sexytime.where = where
        sexytime.save()

        if settings.ECHO:
            resp_data["sexytime"] = obj_sexytimes([sexytime])[0]
        resp_data["status"] = "Success"
    else:
        resp_data["status"] = "Failure"

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# POST /ACTIVITIES/SEXYTIMES/:ID/RSVP/
@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def rsvp_sexytime(request, sexytime_id):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    sexytime_id = int(sexytime_id)
    resp_data = {}

    rsvp = request.POST.get("rsvp", None)

    try:
        sexytime = SexyTime.objects.get(id=sexytime_id)
    except SexyTime.DoesNotExist:
        resp_data["status"] = "Failure"

    if sexytime.p1.id == profile.id or sexytime.p2.id == profile.id:
        if sexytime.p1.id == profile.id and rsvp:
            sexytime.p1_response = "accept"
        else:
            sexytime.p1_response = "reject"
        if sexytime.p2.id == profile.id and rsvp:
            sexytime.p2_response = "accept"
        else:
            sexytime.p2_response = "reject"
        sexytime.save()
        resp_data["status"] = "Success"
        
    if settings.ECHO:
        resp_data["sexytime"] = obj_sexytimes([sexytime])[0]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# POST /ACTIVITIES/SEXYTIMES/:ID/NOTES/ADD/
@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def update_sexytime_note(request, sexytime_id):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    sexytime_id = int(sexytime_id)
    resp_data = {}

    try:
        sexytime = SexyTime.objects.get(id=int(sexytime_id))
    except SexyTime.DoesNotExist:
        resp_data["status"] = "Failure"

    note = request.POST.get("notes", None)
    if not note:
        resp_data["status"] = "Failure"
    else:
        sexytime.notes = note
        sexytime.save()
        resp_data["status"] = "Success"
        if settings.ECHO:
            resp["note"] = {"from": obj_user_summary([profile])[0], "body": note}


    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# POST /ACTIVITIES/WINKS/
@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def create_wink(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))
    resp_data = {}

    wink_id = request.POST.get('winkID', None)
    action = request.POST.get('action', None)
    fb_username = request.POST.get('userID', None)

    if not wink_id:
        to_profile = Profile.objects.has_freya_profile_given_fb_details(fb_username)
        if to_profile:
            wink = Wink()
            wink.to_profile = to_profile
            wink.from_profile = profile
            wink.save()
            resp_data = {}
            resp_data["status"] = "Success" 
            resp_data["wink"] = obj_wink([wink])[0]
    else:
        try:
            wink = Wink.objects.get(id=int(wink_id))
        except Wink.DoesNotExist:
            wink = None

        if wink:
            if action == "hide":
                wink.hide = True
                wink.save()
            elif action == "return":
                wink.accepted = True
                wink.save()
            resp_data["status"] = "Success" 
            resp_data["wink"] = obj_wink([wink])[0]
        else:
            resp_data["status"] = "Failure"

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))