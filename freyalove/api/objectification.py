import facebook

# User
def obj_user(list_of_profiles):
    """
    Given a list of profiles, return a list of dictionaries with the following:
        <user_summary>
        email: String
        fb_id: String
        fb_link: String
        fb_username: String
    """
    assert len(list_of_profiles) > 0, "There must be at least one profile."

    resp = []

    for profile in list_of_profiles:
        profile_as_user = {}
        profile_as_user["id"] = profile.fb_username
        profile_as_user["firstName"] = profile.first_name
        profile_as_user["lastName"] = profile.last_name
        profile_as_user["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
        profile_as_user["points"] = 0 # TODO
        profile_as_user["email"] = profile.email
        profile_as_user["fb_id"] = profile.fb_id
        profile_as_user["fb_link"] = profile.fb_link
        profile_as_user["fb_username"] = profile.fb_username
        resp.append(profile_as_user)

    return resp

# UserSummary
def obj_user_summary(list_of_profiles):
    """
    Given a list of profiles, return a list of dictionaries with the following:
        id: String // by default use verbose userIDs (use FB username)
        firstName: String
        lastName: String
        photo: String
        points: Integer // the points on the leaderboard
    """

    assert len(list_of_profiles) > 0, "There must be at least one profile."

    resp = []

    for profile in list_of_profiles:
        profile_as_user_summary = {}
        profile_as_user_summary["id"] = profile.fb_username
        profile_as_user_summary["firstName"] = profile.first_name
        profile_as_user_summary["lastName"] = profile.last_name
        profile_as_user_summary["photo"] = "http://graph.facebook.com/%s/picture" % profile.fb_username
        profile_as_user_summary["points"] = 0 # TODO
        profile_as_user_summary["username"] = profile.fb_username
        resp.append(profile_as_user_summary)

    return resp

# FbUserSummary
def obj_fb_user_summary(token):
    """
    Given an oauth access token, return a list of dictionaries with the following:
        fb_id: String
        fb_link: String
        fb_username: String
        fb_photo: String
    """
    graph = facebook.GraphAPI(token)
    friends = graph.get_connections("me", "friends")
    friends = friends["data"]

    resp = []
    for f in friends:
        #profile = graph.get_object(f["id"])
        facebook_profile_as_summary = {}
        facebook_profile_as_summary["fb_id"] = f["id"]
        facebook_profile_as_summary["name"] = f["name"]
        #facebook_profile_as_summary["fb_username"] = profile["username"]
        #facebook_profile_as_summary["fb_link"] = "http://www.facebook.com/%s"
        #facebook_profile_as_summary["photo"] = "http://graph.facebook.com/%s/picture" % profile["username"]
        resp.append(facebook_profile_as_summary)

    return resp


## MESSAGES

# ConversationSummary
def obj_message(messages):
    """
    Given a list of messages, return a list of dictionaries with the following:
        id: String
        from: [UserSummary](API-Objects-Messaging#wiki-usersummary)
        to: [UserID]
        date: Timestamp
        body: String
        status: [StatusType](#wiki-statustype)
        timestamp: [DateTime](API-Objects#wiki-datetime)
    """
    resp = []

    for m in messages:
        m_summary = {}
        m_summary["id"] = m.id
        m_summary["from"] = obj_user_summary([m.sender])[0]
        m_summary["to"] = obj_user_summary([m.receiver])[0] # TODO current code implies 1 <-> 1, updated spec is 1 <-> n
        m_summary["date"] = str(m.created_at)
        m_summary["timestamp"] = str(m.created_at) # TODO
        if m.unread:
            m_summary["status"] = "unread"
        elif m.deleted:
            m_summary["status"] = "deleted"
        else:
            m_summary["status"] = "read"

        resp.append(m_summary)

    return resp

def obj_conversation():
    """
    Given, return a list of dictionaries with the following:
        id: String
        participants: [[UserID](Object-API-User#wikiusersummary)]
        status:  [StatusType](#wiki-statustype) // aggregate of the contained messages
        messages: [Message]
    """
    pass

def obj_conversation_summary(conversations):
    """
    Given a list of conversations, return a list of dictionaries with the following:
        id: ConversationID
        participants: [[UserID](Object-API-User#wikiusersummary)]
        status:  [StatusType](#wiki-statustype) // aggregate of the contained messages
        lastMessage: Message
    """
    resp = []
    for c in conversations:
        c_summary = {}
        c_summary["id"] = c.id
        c_summary["participants"] = obj_user_summary([c_summary.owner, c_summary.participant])
        if c.unread:
            c_summary["status"] = "unread"
        elif c.deleted:
            c_summary["status"] = "deleted"
        else:
            c_summary["status"] = "read"
        msgs = c.msg_set.all().order_by('-created_at')
        if msgs.count() > 0:
            c_summary["lastMessage"] = obj_message([msgs[0]])[0]
        else:
            c_summary["lastMessage"] = {}

        resp.append(c_summary)

    return resp

## QUESTIONNAIRE
def obj_questiontopics(qtopics):
    pass

def obj_questiontype(qtypes):
    pass

def obj_questions(questions):
    """
    Given a list of questions, return a list of dictionaries with the following:
    id: String,
    topic: QuestionTopic,
    type: QuestionType,
    question: String,
    helpText: String,
    lang: en
    """
    
    resp = []
    for q in questions:
        q_as_object = {}
        q_as_object["id"] = q.id
        q_as_object["topic"] = q.question_topic.name
        q_as_object["type"] = q.question_type.name
        q_as_object["question"] = q.question_given
        q_as_object["helpText"] = q.help_text
        q_as_object["lang"] = "en"

        resp.append(q_as_object)

    return resp

## ACTIVITIES/NOTIFICATIONS 

def obj_wink(winks):
    resp = []

    for wink in winks:
        wink_as_object = {}
        wink_as_object["id"] = wink.id
        wink_as_object["from"] = obj_user_summary([wink.from_profile])[0]
        wink_as_object["to"] = obj_user_summary([wink.to_profile])[0]
        wink_as_object["type"] = "wink"

        resp.append(wink_as_object)

    return resp

def obj_sexytimes(sexytimes):
    resp = []

    for sexytime in sexytimes:
        sexytime_as_object = {}
        sexytime_as_object["id"] = sexytime.id
        sexytime_as_object["matchmaker"] = obj_user_summary([sexytime.matchmaker])[0]
        if sexytime.p1_attending and sexytime.p1_responded:
            sexytime_as_object["statusFrom"] = "accept"
        elif sexytime.p1_responded and not sexytime.p1_accepted:
            sexytime_as_object["statusFrom"] = "reject"
        else:
            sexytime_as_object["statusFrom"] = "notset"
        if sexytime.p2_attending and sexytime.p2_responded:
            sexytime_as_object["statusTo"] = "accept"
        elif sexytime.p2_responded and not sexytime.p2_accepted:
            sexytime_as_object["statusTo"] = "reject"
        else:
            sexytime_as_object["statusTo"] = "notset"
        sexytime_as_object["when"] = sexytime.when
        sexytime_as_object["where"] = sexytime.where
        sexytime_as_object["notes"] = sexytime.notes

        resp.append(sexytime_as_object)

    return resp

def obj_matches(matches):
    resp = []

    for match in matches:
        match_as_object = {}
        match_as_object["quality"] = match.matchproposal_set.all()[0]
        match_as_object["timestamp"] = match.created_at
        match_as_object["statusFrom"] = match.p1_response
        match_as_object["statusTo"] = match.p2_response

        resp.append(match_as_object)

    return resp

def obj_match_proposals(match_proposals):
    resp = []

    for mp in match_proposals:
        mp_as_object = {}
        mp_as_object["id"] = mp.id
        mp_as_object["from"] = obj_user_summary([mp.from_profile])[0]
        mp_as_object["to"] = obj_user_summary([mp.to_profile])[0]
        mp_as_object["quality"] = mp.quality
        mp_as_object["timestamp"] = mp.timestamp
        resp.append(mp_as_object)

    return resp

def obj_notifications(notes):
    resp = []

    for note in notes:
        note_as_object = {}
        note_as_object["id"] = note.id
        note_as_object["from"] = note.actor
        note_as_object["to"] = note.belongs_to
        note_as_object["type"] = "N/A" # TODO parser
        note_as_object["seen"] = not (note.unread)

        resp.append(note_as_object)

    return resp

def obj_answered_questions(answers):
    resp = []

    for answer in answers:
        answered_question_obj = {}
        answered_question_obj["id"] = answer.question.id
        answered_question_obj["topic"] = answer.question.question_topic.name
        answered_question_obj["type"] = answer.question.question_type.name
        answered_question_obj["question"] = answer.question.question_given
        answered_question_obj["helpText"] = answer.question.help_text
        answered_question_obj["lang"] = "en"
        answered_question_obj["user"] = answer.profile.fb_username
        answered_question_obj["userAnswer"] = answer.answer
        answered_question_obj["matchAnswer"] = answer.matches
        answered_question_obj["comment"] = answer.comment
        answered_question_obj["answerPublic"] = answer.public

        resp.append(answered_question_obj)

    return resp