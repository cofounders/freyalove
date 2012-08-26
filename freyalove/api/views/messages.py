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
from freyalove.api.objectification import obj_message, obj_conversation_summary

@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def conversations(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    conversations = Conversation.objects.fetch_conversations(profile)
    resp_data = obj_conversation_summary(conversations)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def delete_messages(request, username_list):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = {}
    usernames = set(username_list.split("+"))
    if len(usernames) < 1:
        resp_data["status"] = "Failure"
    else:
        current_user_conversations = Conversation.objects.filter(owner=profile)
        for c in current_user_conversations:
            match_usernames = set([p.fb_username for p in c.participants.all()])
            match_usernames.add(c.owner.fb_username)
            if match_usernames == usernames:
                for msg in c.msg_set.all():
                    msg.deleted = True
                    msg.save()

        resp_data["status"] = "Success"

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def fetch_messages(request, username_list):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = []
    usernames = set(username_list.split("+"))
    if len(usernames) < 1:
        pass
    else:
        msgs = []
        current_user_conversations = Conversation.objects.filter(owner=profile)
        for c in current_user_conversations:
            match_usernames = set([p.fb_username for p in c.participants.all()])
            match_usernames.add(c.owner.fb_username)
            if match_usernames == usernames:
                for msg in c.msg_set.all():
                    msgs.append(msg)

        resp_data = obj_message(msgs)

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))

@csrf_exempt
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def send_message(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = {}

    usernames = request.POST.get("to", None)
    msg_body = request.POST.get("body", None)

    if not usernames or len(usernames.split("+")) < 1 or not msg_body:
        resp_data["status"] = "Failure"
    else:
        usernames = usernames.split("+")
        profiles = []
        profiles.append(profile)
        for username in usernames:
            profile = Profile.objects.get(fb_username=username)
            profiles.append(profile)
        has_conversation = Conversation.objects.has_conversation(profiles)
        if has_conversation:
            conversation = Conversation.objects.get_conversation(profiles)
        else:
            conversation = Conversation()
            conversation.save()
        for p in profiles:
            conversation.participants.add(p)
        conversation.owner = profile
        conversation.save()

        # create message
        msg = Msg()
        msg.conversation = conversation
        msg.message = msg_body
        msg.sender = profile
        msg.save()

        resp_data["status"] = "Success"
        resp_data["message"] = obj_message([msg])[0]

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json", status=200))