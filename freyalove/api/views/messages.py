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

def send_message(request):
    if request.method == "POST":
        recipients = request.POST.getlist('to', [])
        message = request.POST.get('body', None)

        if not message or not recipients:
            resp = HttpResponse("Bad request - submission criteria missing.", status=400)
            return resp
        # parse for token in cookie
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)

        if not cookie:
            resp = HttpResponse("Missing authentication cookie", status=403)
            return resp
        profile = is_registered_user(fetch_profile(cookie["access_token"]))

        recipients = [int(x) for x in recipients]

        to_profiles = Profile.objects.filter(id__in=recipients)
        if to_profiles.count() < 1:
            resp = HttpResponse("Bad request - user(s) requested to send message to doesn't exist.", status=400)
            return resp

        resp_data = []

        for to_profile in to_profiles:
            conversation = has_conversation(profile, to_profile)

            msg = Msg()
            msg.message = message
            msg.sender = profile
            msg.receiver = to_profile
            msg.conversation = conversation
            msg.save()

            resp_dict = {}
            resp_dict["id"] = msg.id
            from_summary = {}
            from_summary["id"] = profile.id
            from_summary["firstName"] = profile.first_name
            from_summary["lastName"] = profile.last_name
            from_summary["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
            from_summary["points"] = "N/A"
            resp_dict["from"] = from_summary
            resp_dict["to"] = to_profile.id
            resp_dict["body"] = msg.message
            # TODO: timestamp, status
            resp_data.append(resp_dict)

        resp_json = json.JSONEncoder().encode(resp_data)
        resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
        return resp

    else:
        resp = HttpResponse("Bad request", status=400)
        return resp