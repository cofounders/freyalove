# Registers a note 
from freyalove.notify.models import Note

def notify(profile, verb, content_object=None, actor=None):
    note = Note(
        belongs_to=profile,
        verb=verb
    )
    if content_object:
        note.content_object = content_object
    if actor:
        note.actor = actor

    note.save()
    return note
