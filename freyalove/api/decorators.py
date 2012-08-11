import datetime
import facebook

from django.utils.decorators import available_attrs
from django.conf import settings
from django.http import HttpResponse

def user_is_authenticated_with_facebook(view):
    def _wrapped_view(request, *args, **kwargs):
        # parse for token in cookie
        cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
        if not cookie:
            resp = HttpResponse("Missing authentication cookie", status=403)
            return resp
        else:
            return view(request, *args, **kwargs)
    return _wrapped_view