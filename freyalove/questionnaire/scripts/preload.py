# Preload questionnaire content from Karen
# This script will preload the structure into the database (if not already done; else this script is safe to re-run multiple times)


# import Questionnaire models
from freyalove.questionnaire.models import QuestionTopic, QuestionType

# Rigid Topics
RIGID_TOPICS = (
	"about",
	"looks",
	"background",
)

# Extensible Topics
EXTENSIBLE_TOPICS = (
	"lifestyle",
	"relationship",
	"personality",
	"sexualstyle",
)

# Create Topics
for topic in RIGID_TOPICS + EXTENSIBLE_TOPICS:
	try:
		qtopic = QuestionTopic.objects.get(name=topic)
	except QuestionTopic.DoesNotExist:
		qtopic = None

	if not qtopic:
		qtopic = QuestionTopic(name=topic)
		qtopic.save()

# Types
QUESTION_TYPES = (
	"checkbox",
	"float",
	"fourAnswer",
	"radio",
	"scale",
	"textarea",
)

# Create Types
for qtype in QUESTION_TYPES:
	try:
		questiontype = QuestionType.objects.get(name=qtype)
	except QuestionType.DoesNotExist:
		questiontype = None

	if not questiontype:
		questiontype = QuestionType(name=qtype)
		questiontype.save()