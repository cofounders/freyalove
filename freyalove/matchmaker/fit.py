from freyalove.users.models import Profile, Wink
from freyalove.questionnaire.models import Question, Answer
# ref: https://github.com/cofounders/freyalove/wiki/Algorithm-Match-Fit

def match_fit(profile_1, profile_2):
    """
    Calculates a score (0 - 100) based on questions answered by 2 profiles.
    """

    score = 0.0
    # Scoring formula: OverallMatchQuality := (sum(QuestionPoints)/Number of Questions))/2 + {0.2 || 0}


    # Fetch mutually answered questions
    questions = Answer.objects.mutual_questions(profile_1, profile_2)
    n = len(questions)
    question_points = 0.0

    for q in questions:
        p1_answer = Answer.objects.get(question=q, profile=profile_1)
        p2_answer = Answer.objects.get(question=q, profile=profile_2)

        if p1_answer.answer in p2_answer.matches and p2_answer.answer in p1_answer.matches:
            question_points += 0.2
        elif p1_answer.answer in p2_answer.matches or p2_answer.answer in p1_answer.matches:
            question_points += 0.1
        else:
            pass

    score += ((questions_points/n)/2)

    # A mutual wink adds 20%
    if Wink.objects.has_wink(profile_1, profile_2):
        if score <= :
            score += .2
        else:
            score = 1.0
    return score * 100.0
