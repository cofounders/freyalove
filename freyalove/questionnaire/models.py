from django.db import models

from freyalove.users.models import Profile
from freyalove.questionnaire.managers import QuestionnaireManager

class QuestionTopic(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class QuestionType(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Question(models.Model):
    question_topic = models.ForeignKey(QuestionTopic)
    question_type = models.ForeignKey(QuestionType)
    question_given = models.CharField(max_length=300)
    choice_1 = models.CharField(max_length=300, blank=True)
    choice_2 = models.CharField(max_length=300, blank=True)
    choice_3 = models.CharField(max_length=300, blank=True)
    choice_4 = models.CharField(max_length=300, blank=True)
    help_text = models.TextField(blank=True)
    publish = models.BooleanField(default=True)

    objects = QuestionnaireManager()

    def __unicode__(self):
        return "%s / %s / %d" % (self.question_topic, self.question_type, self.id)

# Questions defined in https://github.com/cofounders/freyalove/wiki/API-Objects-Questionnaire (medium - high priority)
class Answer(Question):
    profile = models.ForeignKey(Profile)
    question = models.ForeignKey(Question, related_name="for_question")
    answer = models.CharField(max_length=300, blank=True)
    matches = models.CharField(max_length=300, blank=True)
    comment = models.TextField(blank=True)
    public = models.BooleanField(default=False)
