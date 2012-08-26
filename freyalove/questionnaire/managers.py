# Complex manager for Questionnaire to help cope with all the various formats.

from django.db import models

class QuestionnaireManager(models.Manager):
	# stub
	pass

class AnswerManager(models.Manager):
	def mutual_questions(self, profile_1, profile_2):
		# Returns mutually answered questions between 2 profiles
		answers_1 = super(AnswerManager, self).get_query_set().filter(profile=profile_1)
		answers_2 = super(AnswerManager, self).get_query_set().filter(profile=profile_2)

		mutual_questions = set([answer.question for answer in answers_1] + [answer.question.id for answer in answers_2])

		return mutual_questions