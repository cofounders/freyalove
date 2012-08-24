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

def obj_wink(winks):
    resp = []

    for wink in winks:
        wink_as_object = {}
        wink_as_object["wink_id"] = wink.id
        wink_as_object["from"] = obj_user_summary([wink.from_profile])[0]
        wink_as_object["to"] = obj_user_summary([wink.to_profile])[0]
        wink_as_object["type"] = "wink"

        resp.append(wink_as_object)

    return resp