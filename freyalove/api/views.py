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
from freyalove.users.models import Profile, Blocked, Friendship, Wink
from freyalove.matchmaker.models import Match, SexyTime

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
    #   resp = HttpResponse("Cookie not set", status=404)
    #   return resp

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

def fetch_winks(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Cookie not set", status=404)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    winks = Wink.objects.filter(to_profile=profile)

    resp_data = {}
    resp_data["winks"] = []
    for w in winks:
        resp_data["winks"].append({"from": w.from_profile.first_name})
        # we write a generator for throwing up a UserSummary next

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp

def fetch_activities(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Cookie not set", status=404)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    winks = Wink.objects.filter(to_profile=profile)
    sexytimes = SexyTime.objects.fetch_sexytimes(profile)

    resp_data = {}
    resp_data["activities"] = []

    for w in winks:
        resp_data["activities"].append({"type": "wink", "from": w.from_profile.id, "to": w.to_profile.id})

    for s in sexytimes:
        resp_data["activities"].append({"type": "sexytime", "p2": s.p2.id, "p1": s.p1.id, "when": s.when, "where": s.where})

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
            resp = HttpResponse("Cookie not set", status=404)
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
            resp = HttpResponse("Cookie not set", status=404)
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
def create_wink(request, from_profile_id, to_profile_id):
    if request.method == "POST":
        resp_data = {}

        # parse for token in cookie
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)

        if not cookie:
            resp = HttpResponse("Cookie not set", status=404)
            return resp
        profile = is_registered_user(fetch_profile(cookie["access_token"]))

        if profile.id != int(from_profile_id):
            resp = HttpResponse("Bad request - from user must match current profile (current %d, from %d)" % (profile.id, int(from_profile_id)), status=400)
            return resp

        try:
            to_profile = Profile.objects.get(id=int(to_profile_id))
        except Profile.DoesNotExist:
            to_profile = None
            resp = HttpResponse("Bad request - to user doesn't exist!", status=400)
            return resp

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

