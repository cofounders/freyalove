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

def fetch_messages(request, conversation_id):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    try:
        conversation = Conversation.objects.get(id=int(conversation_id))
    except Conversation.DoesNotExist:
        resp = HttpResponse("Conversation does not exist!", status=404)
        return resp

    if conversation.owner == profile or conversation.participant == profile:
        pass
    else:
        resp = HttpResponse("Invalid profile.", status=400)
        return resp

    resp_data = {}
    resp_data["messages"] = []

    messages = Msg.objects.get(conversation=conversation).order_by('-created_at')

    for m in messages:
        from_profile = {}
        to_profile = {}

        from_profile["name"] = m.sender.first_name + " " + m.sender.last_name
        from_profile["id"] = m.sender.id
        from_profile["photo"] = "http://graph.facebook.com/%s/picture" % m.sender.fb_username

        to_profile["name"] = m.receiver.first_name + " " + m.receiver.last_name
        to_profile["id"] = m.receiver.id
        to_profile["photo"] = "http://graph.facebook.com/%s/picture" % m.receiver.fb_username

        resp_data["messages"].append({
            "from": from_profile,
            "to": to_profile,
            "body": m.message,
            "status": "N/A",
        })

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp 

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