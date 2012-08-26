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

from freyalove.users.models import Profile, Wink, ProfileDetail, ProfilePrivacyDetail, Friendship
from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import obj_user_summary, obj_user, obj_fb_user_summary

# GET /PROFILE/DETAILS/
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
        try:
            resp_data[field] = getattr(profile.details, field)
        except AttributeError:
            pass
    for field in privacy_fields:
        try:
            resp_data[field + "Public"] = getattr(profile.permissions, field)
        except AttributeError:
            pass

    # TODO: We should match the introspection against a whitelist

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# GET /PROFILE/
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

    resp_data_ = obj_user([profile])
    resp_data = resp_data_[0]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# POST /PROFILE/
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

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# POST /PROFILE/UNREGISTER/
@csrf_exempt
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

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# Not activated, for in case manual points assignment is called for
# POST /PROFILE/POINTS/ADD/
@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def add_points(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = existing_user(fetch_profile(cookie["access_token"]))

    points = request.POST.get("points", None)

    if points:
        points = int(points)
        profile.matchmaker_score += points
        profile.save()

    resp_data = obj_user_summary([profile])[0]
    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# GET /USERS/FACEBOOKFRIENDS/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def facebookfriends(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = existing_user(fetch_profile(cookie["access_token"]))

    resp_data = obj_fb_user_summary(cookie["access_token"])
    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

# GET /USERS/SEARCH/:QUERY/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def search(request, query):
    query = request.GET.get("q", None)
    resp_data = []

    #query = parse_term(query)
    if query:
        profiles = Profile.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        if profiles.count() > 0:
            resp_data = obj_user_summary(profiles)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200)) 

# GET /USERS/FRIENDS/LEADERBOARD/SUMMARY/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def leaderboard(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = existing_user(fetch_profile(cookie["access_token"]))

    friends_ids = [f.id for f in Friendship.objects.friends_for_profile(profile)]
    friend_profiles = Profile.objects.filter(id__in=friends_ids).order_by('-matchmaker_score')

    if friend_profiles.count() <= 5:
        pass
    else:
        friend_profiles = friend_profiles[:5]

    resp_data = obj_user_summary(friend_profiles)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200)) 
    
