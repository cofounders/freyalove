try:
    import json
except ImportError:
    import simplejson as json

import datetime
from functools import wraps
import facebook

from django.utils.decorators import available_attrs
from django.conf import settings
from django.http import HttpResponse

from freyalove.users.models import Profile, Blocked, Friendship, ProfileDetail, ProfilePrivacyDetail
from freyalove.matchmaker.models import Match
from freyalove.conversations.models import Conversation

# Utils
def inject_cors(resp_obj):
    resp_obj['Access-Control-Allow-Origin'] = '*'
    resp_obj['Access-Control-Allow-Headers'] = 'Authorization'

    # usually used in preflight, but we just give it all the time
    resp_obj['Access-Control-Allow-Methods'] = 'GET,POST,PUT'
    resp_obj['Access-Control-Allow-Credentials'] = 'true'

    return resp_obj

def is_registered_user(profile_dict):
    """
    Checks if a user is already registered with us, if not, we register her
    """
    if profile_dict:
        fb_id = profile_dict["id"]
        try:
            profile = Profile.objects.get(fb_id=fb_id)
            if profile.details:
                pass
            else:
                details = ProfileDetail()
                details.save()
                profile.details = details
                profile.save()
            if profile.permissions:
                pass
            else:
                permissions = ProfilePrivacyDetail()
                permissions.save()
                profile.permissions = permissions
                profile.save()
            return profile
        except Profile.DoesNotExist:
            profile = create_freya_profile(profile_dict)
            return profile

def existing_user(profile_dict):
    """
    Checks if a user is already registered with us, if not, don't register her
    """
    if profile_dict:
        fb_id = profile_dict["id"]
        try:
            profile = Profile.objects.get(fb_id=fb_id)
            if profile.details:
                pass
            else:
                details = ProfileDetail()
                details.save()
                profile.details = details
                profile.save()
            if profile.permissions:
                pass
            else:
                permissions = ProfilePrivacyDetail()
                permissions.save()
                profile.permissions = permissions
                profile.save()
            return profile
        except Profile.DoesNotExist:
            return None

def create_freya_profile(profile_dict):
    profile = Profile()
    profile.first_name = profile_dict["first_name"]
    profile.last_name = profile_dict["last_name"]
    profile.fb_id = profile_dict["id"]
    profile.fb_username = profile_dict.get("username", profile_dict["id"])
    profile.fb_link = profile_dict["link"]
    profile.email = profile_dict["email"]
    profile.save()
    return profile

def convert_to_dtobj(txt_date):
    return datetime.datetime.now()

def has_conversation(from_profile, to_profile):
    try:
        conversation = Conversation.objects.get(owner=from_profile, participant=to_profile)
    except Conversation.DoesNotExist:
        conversation = Conversation()
        conversation.owner = from_profile
        conversation.participant = to_profile
        conversation.save()

    return conversation

def parse_term(term):
    return " ".join(term.split("+"))

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