from freyalove.users.models import Profile, Blocked, Friendship, ProfileDetail, ProfilePrivacyDetail
from freyalove.matchmaker.models import Match
from freyalove.conversations.models import Conversation

import datetime

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

def get_user(fb_username_or_id):
    profile = None
    # filler function until transition to verbose username complete
    try:
        fb_id = int(fb_username_or_id)
    except ValueError:
        fb_id = None

    if not fb_id:
        try:
            profile = Profile.objects.get(fb_username=fb_username_or_id)
        except Profile.DoesNotExist:
            pass
    else:
        try:
            profile = Profile.objects.get(fb_id=fb_id)
        except Profile.DoesNotExist:
            pass

    return profile

def create_freya_profile(profile_dict):
    profile = Profile()
    profile.first_name = profile_dict["first_name"]
    profile.last_name = profile_dict["last_name"]
    profile.fb_id = profile_dict["id"]
    profile.fb_username = profile_dict["username"]
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