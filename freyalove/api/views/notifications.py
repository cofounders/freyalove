from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

try:
    import json
except ImportError:
    import simplejson as json

import facebook

from freyalove.users.models import Profile, Wink, ProfileDetail, ProfilePrivacyDetail
from freyalove.notify.models import Note
from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import *

# GET /NOTIFICATIONS/UNREAD/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def unread(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    resp_data = obj_notification(Note.objects.filter(belongs_to=profile, unread=True))

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))