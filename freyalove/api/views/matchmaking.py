from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

try:
    import json
except ImportError:
    import simplejson as json

import facebook

from freyalove.users.models import Profile, Friendship
from freyalove.matchmaker.models import Match, MatchProposal
from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import *

# POST /MATCHMAKER/MATCH/
@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def match(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    from_profile = request.POST.get('from', None)
    to_profile = request.POST.get('to', None)

    resp_data = {}

    if not from_profile or not to_profile:
    	resp["status"] = "Failure"

    from_profile = Profile.objects.get(fb_username=from_profile)
    to_profile = Profile.objects.get(fb_username=to_profile)

    if not Friendship.objects.are_friends(from_profile, to_profile):
    	pass
    else:
    	match = Match()
    	match.matchmaker = profile
    	match.p1 = from_profile
    	match.p2 = to_profile
    	match.save()

    	proposal = MatchProposal()
    	proposal.from_profile = from_profile
    	proposal.to_profile = to_profile
    	proposal.quality = int(69)
    	proposal.match = match
    	proposal.save()

    	resp_data["match"] = obj_matches([match])[0]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# GET /MATCHMAKER/RECOMMENDATIONS/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def recommendations(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    friends = Friendship.objects.friends_for_profile(profile)
    friends_ids = [f.id for f in friends]

    proposals = MatchProposal.objects.filter(to_profile__in=friends_ids, from_profile__in=friends_ids).order_by('-quality')
    rejected_ids = []
    for p in proposals:
        if p.match.rejected:
            rejected_ids.append(p.id)
    proposals = proposals.exclude(id__in=rejected_ids)
    resp_data = obj_match_proposals(proposals)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# GET /MATCHMAKER/:USERNAME_LIST/QUESTIONS/ANSWERED/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def answered(request, username_list):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    usernames = username_list.split("+")
    verified_profiles = []
    for username in usernames:
        friend_profile = Profile.objects.has_freya_profile_given_fb_details(username)
        if friend_profile:
            if Friendship.objects.are_friends(profile, friend_profile):
                verified_profiles.append(friend_profile)

    answers = []
    for p in verified_profiles:
        answers += list(Answer.objects.filter(profile=p))

    resp_data = obj_answered_questions(answers)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))