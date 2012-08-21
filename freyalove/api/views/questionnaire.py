from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q

try:
    import json
except ImportError:
    import simplejson as json

import facebook
import random

from freyalove.users.models import Profile, Wink, ProfileDetail, ProfilePrivacyDetail, Friendship
from freyalove.questionnaire.models import QuestionTopic, QuestionType, Question, Answer
from freyalove.api.decorators import user_is_authenticated_with_facebook
from freyalove.api.utils import *
from freyalove.api.objectification import obj_user_summary, obj_user, obj_fb_user_summary, obj_question

# GET /USERS/:USERNAME/QUESTIONNAIRE/CATEGORIES/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def categories(request, fb_username):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    other_profile = Profile.objects.get(fb_username=fb_username)
    are_friends = Friendship.objects.are_friends(profile, other_profile)
    resp_data = []

    if not are_friends:
        return HttpResponse("Not friends", status=403)

    answers = Answer.objects.filter(profile=other_profile)
    for ans in answers:
        resp_data.append(ans.question.question_topic.name)

    resp_data = list(set(resp_data))
    
    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# GET /USERS/:USERNAME/QUESTIONNAIRE/{CATEGORY}/{ANSWERED|UNANSWERED}/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def random_questions(request, fb_username, category, status):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    other_profile = Profile.objects.get(fb_username=fb_username)
    are_friends = Friendship.objects.are_friends(profile, other_profile)
    resp_data = []

    topic = QuestionTopic.objects.get(name=category)

    if not are_friends:
        return HttpResponse("Not friends", status=403)

    if status == "answered":
        questions = Question.objects.filter(question_topic=topic)
        answers = []
        for q in questions:
            try:
                answered = Answer.objects.get(question=q, profile=other_profile)
            except Answer.DoesNotExist:
                answered = None
            if answered:
                answers.append(answered)

        random.shuffle(answers)
        resp_data.append(obj_question([answers[0].question])[0])

    elif status == "unanswered":
        questions = Question.objects.filter(question_topic=topic)
        answers = []
        for q in questions:
            try:
                answered = Answer.objects.get(question=q, profile=other_profile)
            except Answer.DoesNotExist:
                answered = None
            if not answered:
                answers.append(q)

        random.shuffle(answers)
        resp_data.append(obj_question([answers[0]])[0])
    else:
        # throw error
        raise Http404

    # TODO: Clarify with Wolf if AnsweredQuestion objects should be returned only (since it includes the question data)
    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

# GET /USERS/:USERNAME/QUESTIONNAIRE/QUESTIONS/RANDOM/{ANSWERED|UNANSWERED}/
@user_is_authenticated_with_facebook
@require_http_methods(["GET"])
def random_questions(request, fb_username, status):
    cookie = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_ID, settings.FACEBOOK_SECRET)
    profile = is_registered_user(fetch_profile(cookie["access_token"]))

    other_profile = Profile.objects.get(fb_username=fb_username)
    are_friends = Friendship.objects.are_friends(profile, other_profile)
    resp_data = []

    topics = QuestionTopic.objects.all()

    if not are_friends:
        return HttpResponse("Not friends", status=403)

    if status == "answered":
        for topic in topics:
            questions = Question.objects.filter(question_topic=topic)
            answers = []
            for q in questions:
                try:
                    answered = Answer.objects.get(question=q, profile=other_profile)
                except Answer.DoesNotExist:
                    answered = None
                if answered:
                    answers.append(answered)

            random.shuffle(answers)
            resp_data.append(obj_question([answers[0].question])[0])

    elif status == "unanswered":
        for topic in topics:
            questions = Question.objects.filter(question_topic=topic)
            answers = []
            for q in questions:
                try:
                    answered = Answer.objects.get(question=q, profile=other_profile)
                except Answer.DoesNotExist:
                    answered = None
                if not answered:
                    answers.append(q)

            random.shuffle(answers)
            resp_data.append(obj_question([answers[0]])[0])
    else:
        # throw error
        raise Http404

    return inject_cors(HttpResponse(json.JSONEncoder().encode(resp_data), content_type="application/json"))

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