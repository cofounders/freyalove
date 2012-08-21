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

from freyalove.users.models import Profile, Wink, ProfileDetail, ProfilePrivacyDetail
from freyalove.questionnaire.models import QuestionTopic, QuestionType, Question, Answer
from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import obj_user_summary, obj_user, obj_fb_user_summary

# POST /QUESTIONNAIRE/QUESTIONS/ADD/
@user_is_authenticated_with_facebook
@require_http_methods(["POST"])
def answer(request):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    answer = Answer()
    resp_data = {}
    answer.profile = profile

    # parse POST values
    question = Question.objects.get(id=int(request.POST.get('id', None)))
    answer = request.POST.get('userAnswer', None)
    matches = request.POST.get('matchAnswer', None)
    public = request.POST.get('answerPublic', None)
    comment = request.POST.get('comment', None)

    answer.question = question
    if not answer:
        resp_data["status"] = "Fail"
    else:
        answer.answer = answer
        answer.matches = matches
        answer.public = public
        if comment:
            answer.comment = comment

        answer.save()
        resp_data["status"] = "Success"

    if settings.ECHO:
        # TODO echo back AnsweredQuestion object
        pass

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))