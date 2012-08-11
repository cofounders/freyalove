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
        profile = graph.get_object(f["id"])
        facebook_profile_as_summary = {}
        facebook_profile_as_summary["fb_id"] = profile["id"]
        facebook_profile_as_summary["fb_username"] = profile["username"]
        facebook_profile_as_summary["fb_link"] = "http://www.facebook.com/%s"
        facebook_profile_as_summary["photo"] = "http://graph.facebook.com/%s/picture" % profile["username"]
        resp.append(facebook_profile_as_summary)
        
    return friends