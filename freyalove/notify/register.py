# Registers a note 
from freyalove.notify.models import Note

def notify(profile, verb, content_object, actor=None):
	note = Note(
		belongs_to=profile,
		verb=verb,
		content_object=content_object
	)
	if actor:
		note.actor = actor

	note.save()
	return note
