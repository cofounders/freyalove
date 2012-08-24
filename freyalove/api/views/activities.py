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

from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import obj_user_summary, obj_user, obj_fb_user_summary, obj_wink

def fetch_sexytimes(request):
    """
    Returns all incoming sexytimes for a user.
    """

    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
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

# GET /ACITIVITIES/WINKS/UNRETURNED/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def fetch_winks(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    winks = Wink.objects.filter(to_profile=profile, accepted=False)

    resp_data = obj_wink(winks)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

def fetch_activities(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    winks = Wink.objects.filter(to_profile=profile)
    sexytimes = SexyTime.objects.fetch_sexytimes(profile)

    resp_data = {}
    resp_data["activities"] = []

    for w in winks:
        resp_data["activities"].append({"type": "wink", "from": w.from_profile.id, "to": w.to_profile.id})

    for s in sexytimes:
        resp_data["activities"].append({"type": "sexytime", "p2": s.p2.id, "p1": s.p1.id, "when": str(s.when), "where": s.where})

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp

@csrf_exempt
def create_sexytime(request):
    if request.method == "POST":
        resp_data = {}

        p1 = request.POST.get("from", None)
        p2 = request.POST.get("to", None)
        when = request.POST.get("when", None)
        where = request.POST.get("where", None)

        if p1 and p2 and when and where:
            # does users exists?
            try:
                p1_profile = Profile.objects.get(id=int(p1))
            except Profile.DoesNotExist:
                p1_profile = None
                resp["status"] = "Fail. User of id %s does not exist!" % p1
            try:
                p2_profile = Profile.objects.get(id=int(p2))
            except Profile.DoesNotExist:
                p2_profile = None
                resp["status"] = "Fail. User of id %s does not exist!" % p2

            # parse date
            when_parsed = convert_to_dtobj(when)

            sexytime = SexyTime()
            sexytime.p1 = p1_profile
            sexytime.p2 = p2_profile
            sexytime.when = when_parsed
            sexytime.where = where
            sexytime.save()

            resp_data["sexytime_id"] = sexytime.id
            resp_data["status"] = "Success. SexyTime between %s and %s created." % (p1_profile.id, p2_profile.id)
        else:
            resp_data["status"] = "Fail. You did not provide all fields required."

        resp_json = json.JSONEncoder().encode(resp_data)
        resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
        return resp
    else:
        resp = HttpResponse("Bad request", status=400)
        return resp

@csrf_exempt
def rsvp_sexytime(request, sexytime_id):
    if request.method == "POST":
        sexytime_id = int(sexytime_id)
        resp_data = {}

        # parse for token in cookie
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
        if not cookie:
            resp = HttpResponse("Missing authentication cookie", status=403)
            return resp

        profile = is_registered_user(fetch_profile(cookie["access_token"]))
        try:
            sexytime = SexyTime.objects.get(id=sexytime_id)
        except SexyTime.DoesNotExist:
            resp = HttpResponse("SexyTime requested does not exist!", status=404)
            return resp

        if sexytime.p1.id == profile.id or sexytime.p2.id == profile.id:
            if sexytime.p1.id == profile.id:
                sexytime.p1_attending = True
                sexytime.p1_responded = True
            else:
                sexytime.p2_attending = True
                sexytime.p2_responded = True
            sexytime.save()
            resp_data["status"] = "RSVP for event %d, participant %d successful!" % (sexytime.id, profile.id)
            resp_json = json.JSONEncoder().encode(resp_data)
            resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
            return resp
        else:
            resp = HttpResponse("You are trying to RSVP for a sexytime you're not part of!", status=400)
            return resp
    else:
        resp = HttpResponse("Bad request", status=400)
        return resp

@csrf_exempt
def update_sexytime_note(request, sexytime_id):
    if request.method == "POST":
        sexytime_id = int(sexytime_id)
        resp_data = {}

        # parse for token in cookie
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
        if not cookie:
            resp = HttpResponse("Missing authentication cookie", status=403)
            return resp

        profile = is_registered_user(fetch_profile(cookie["access_token"]))

        try:
            sexytime = SexyTime.objects.get(id=int(sexytime_id))
        except SexyTime.DoesNotExist:
            resp = HttpResponse("SexyTime requested does not exist!", status=404)
            return resp

        note = request.POST.get("notes", None)
        if not note:
            resp_data["status"] = "Fail"
        else:
            sexytime.notes = note
            sexytime.save()
            resp_data["status"] = "Successfully updated note for sexytime %d" % sexytime.id
            resp_data["note"] = sexytime.notes

        resp_json = json.JSONEncoder().encode(resp_data)
        resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
        return resp
    else:
        resp = HttpResponse("Bad request", status=400)
        return resp

@csrf_exempt
def create_wink(request, to_profile_id):
    if request.method == "POST":
        resp_data = {}

        # parse for token in cookie
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)

        if not cookie:
            resp = HttpResponse("Missing authentication cookie", status=403)
            return resp
        profile = is_registered_user(fetch_profile(cookie["access_token"]))

        try:
            to_profile = Profile.objects.get(id=int(to_profile_id))
        except Profile.DoesNotExist:
            to_profile = None
            resp = HttpResponse("Bad request - to user doesn't exist!", status=400)
            return resp

        try:
            wink = Wink.objects.get(from_profile=profile, to_profile=to_profile, received=False)
            resp = HttpResponse("Bad request - a wink already exists!", status=400)
            return resp
        except Wink.DoesNotExist:
            pass

        wink = Wink()
        wink.to_profile = to_profile
        wink.from_profile = profile
        wink.save()
        resp_data = {}
        resp_data["status"] = "Successfully create a wink from %d to %d" % (wink.from_profile.id, wink.to_profile.id)
        resp_json = json.JSONEncoder().encode(resp_data)
        resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
        return resp
    else:
        resp = HttpResponse("Bad request", status=400)
        return resp