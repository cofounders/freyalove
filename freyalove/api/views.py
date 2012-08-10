# We're only going to be using this API internally, so we can safely assume that JSON is only format required.
# That being laid on, we should try and adhere to not repeating bad stuff outlined by @jacobian 
# See: http://jacobian.org/writing/rest-worst-practices/

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

#from freyalove.matchmaker.models import MatchMaker
from freyalove.users.models import Profile, Blocked, Friendship, Wink, ProfileDetail, ProfilePrivacyDetail
from freyalove.matchmaker.models import Match, SexyTime
from freyalove.conversations.models import Conversation, Msg

from freyalove.api.utils import *


# GET
def hello(request):
    resp_data = {"hello": "api"}
    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
    return resp

def profile_summary(request):
    """
    Return summarized information on a user profile given an id/fb_id
    """
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = {}
    resp_data["id"] = profile.id
    resp_data["firstName"] = profile.first_name 
    resp_data["lastName"] = profile.last_name 
    resp_data["email"] = profile.email
    resp_data["fb_id"] = profile.fb_id
    resp_data["fb_link"] = profile.fb_link
    resp_data["fb_username"] = profile.fb_username
    #resp_data["photo"] = fetch_profile_picture(token)
    resp_data["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
    resp_json = json.JSONEncoder().encode(resp_data)

    resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
    return resp

def profile_details(request):
    """
    Return summarized information on a user profile given an id/fb_id
    """
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = {}
    
    details_fields = ProfileDetail._meta.get_all_field_names()
    privacy_fields = ProfilePrivacyDetail._meta.get_all_field_names()
    for field in details_fields:
        resp_data[field] = getattr(profile.details, field)
    for field in privacy_fields:
        resp_data[field + "Public"] = getattr(profile.permissions, field)
    resp_json = json.JSONEncoder().encode(resp_data)

    resp = inject_cors(HttpResponse(resp_json, content_type="application/json"))
    return resp

def profile(request):
    """
    Return information on a user profile given an id/fb_id
    """
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

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
        resp = HttpResponse("Missing authentication cookie", status=403)
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
        resp = HttpResponse("Missing authentication cookie", status=403)
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
        resp = HttpResponse("Missing authentication cookie", status=403)
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

def fetch_winks(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
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

def fetch_conversations(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    conversations = Conversation.objects.fetch_conversations(profile)

    resp_data = {}
    resp_data["conversations"] = []

    for c in conversations:
        last_message = Msg.objects.filter(conversation=c).order_by('-created_at')
        from_profile = {}
        to_profile = {}

        from_profile["name"] = last_message.sender.first_name + " " + last_message.sender.last_name
        from_profile["id"] = last_message.sender.id
        from_profile["photo"] = "http://graph.facebook.com/%s/picture" % last_message.sender.fb_username

        to_profile["name"] = last_message.receiver.first_name + " " + last_message.receiver.last_name
        to_profile["id"] = last_message.receiver.id
        to_profile["photo"] = "http://graph.facebook.com/%s/picture" % last_message.receiver.fb_username

        resp_data["conversations"].append({
            "status":"N/A", 
            "lastMessage": 
            {
                "from": from_profile,
                "to": to_profile,
                "body": last_message.message,
                "status": "N/A",
            }
        })
    # return the following
    # [ConversationSummary]
    """
    ConversationSummary: {
        status: ConversationStatus,
        lastMessage: Message
    }

    @kenny: for additional info::
    Message: {
        from: UserSummary,
        to: UserSummary,
        body: String,
        status: ConversationStatus
    }

    UserSummary: {
        name: String,
        id: String,
        photo: String
    }
    """

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp

def fetch_unread_conversations(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    conversations = Conversation.objects.fetch_unread_conversations(profile)

    resp_data = {}
    resp_data["conversations"] = []

    for c in conversations:
        last_message = Msg.objects.filter(conversation=c).order_by('-created_at')
        from_profile = {}
        to_profile = {}

        from_profile["name"] = last_message.sender.first_name + " " + last_message.sender.last_name
        from_profile["id"] = last_message.sender.id
        from_profile["photo"] = "http://graph.facebook.com/%s/picture" % last_message.sender.fb_username

        to_profile["name"] = last_message.receiver.first_name + " " + last_message.receiver.last_name
        to_profile["id"] = last_message.receiver.id
        to_profile["photo"] = "http://graph.facebook.com/%s/picture" % last_message.receiver.fb_username

        resp_data["conversations"].append({
            "status":"N/A", 
            "lastMessage": 
            {
                "from": from_profile,
                "to": to_profile,
                "body": last_message.message,
                "status": "N/A",
            }
        })

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp

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

def search(request):
    query = request.GET.get('q', None)
    resp_data = []

    if not query:
        pass
    else:
        profiles = Profile.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        for profile in profiles:
            resp_dict = {}
            resp_dict["id"] = profile.id
            resp_dict["name"] = profile.first_name + " " + profile.last_name # TODO: privacy guides the concat?
            resp_dict["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
            resp_dict["points"] = "N/A" # not yet implemented
            resp_data.append(resp_dict)

    resp_json = json.JSONEncoder().encode(resp_data)
    resp = inject_cors(HttpResponse(resp_json, content_type="application/json", status=200))
    return resp 

# POST
@csrf_exempt
def update_profile(request):
    # parse for token in cookie
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    if not cookie:
        resp = HttpResponse("Missing authentication cookie", status=403)
        return resp

    profile = is_registered_user(fetch_profile(cookie["access_token"]))

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

def profile_unregister(request):
    """
    Allows the user to delete the Freya Love account. 
    A successful request to this URL deletes the account and all data stored with it. 
    The fb_id is sent only for confirmation purposes.
    """
    # parse for token in cookie
    if request.method == "POST":
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
        if not cookie:
            resp = HttpResponse("Missing authentication cookie", status=403)
            return resp

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

