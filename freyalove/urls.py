from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Django Admin urls
    url(r'^nimdatux/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    # CURRENT USER
    url(r'^profile/details/$', 'freyalove.api.views.currentuser.profile_details'),
    url(r'^profile/unregister/$', 'freyalove.api.currentuser.views.profile_unregister'),
    url(r'^profile/$', 'freyalove.api.views.currentuser.profile'),
    url(r'^users/facebookfriends/$', 'freyalove.api.views.currentuser.facebookfriends'),
    url(r'^users/search/(?P<query>[-\w+]+)/$', 'freyalove.api.views.currentuser.search'), 
    url(r'^users/friends/leaderboard/summary/$', 'freyalove.api.views.currentuser.leaderboard'),

    # OTHER USERS
    url(r'^users/(?P<fb_username>[-\w]+)/profile/$', 'freyalove.api.views.otherusers.profile'),
    url(r'^users/(?P<fb_username>[-\w]+)/profile/summary/$', 'freyalove.api.views.otherusers.profile_summary'),
    url(r'^users/(?P<fb_username>[-\w]+)/friends/$', 'freyalove.api.views.otherusers.friends'),
    url(r'^users/friends/(?P<fb_username>[-\w]+)/mutual/$', 'freyalove.api.views.otherusers.mutual_friends'),

    # ACTIVITIES
    url(r'^activities/sexytimes/upcoming/$', 'freyalove.api.views.activities.fetch_sexytimes'), 
    url(r'^activities/winks/unreturned/$', 'freyalove.api.views.activities.fetch_winks'),
    url(r'^activities/$', 'freyalove.api.views.activities.fetch_activities'), # winks and sexytimes combined
    url(r'^activities/sexytimes/create/$', 'freyalove.api.views.activities.create_sexytime'), # create SexyTime
    url(r'^activities/sexytimes/(\d+)/rsvp/$', 'freyalove.api.views.activities.rsvp_sexytime'), # rsvp for a SexyTime
    url(r'^activities/sexytimes/(\d+)/notes/add/$', 'freyalove.api.views.activities.update_sexytime_note'),
    url(r'^activities/winks/to/(\d+)/$', 'freyalove.api.views.activities.create_wink'), # send Wink

    # MESSAGES
    url(r'^conversations/$', 'freyalove.api.views.messages.conversations'),
    url(r'^conversations/(?P<username_list>[-\w+]+)/delete/$', 'freyalove.api.views.messages.delete_messages'),
    url(r'^conversations/(?P<username_list>[-\w+]+)/messages/$', 'freyalove.api.views.messages.fetch_messages'),
    url(r'^conversations/message/$', 'freyalove.api.views.messages.send_message'),

    # STREAM
    url(r'^stream/unread/$', 'freyalove.api.views.stream.unread'),

    # MATCHMAKING
    url(r'^matchmaker/recommendations/$', 'freyalove.api.views.matchmaking.recommendations'),
    url(r'^matchmaker/match/$', 'freyalove.api.views.matchmaking.match'),
    url(r'^matchmaker/(?P<userid_list>[-\w+]+)/questions/answered/$', 'freyalove.api.views.matchmaking.answered'),

    # QUESTIONNAIRE
    url(r'^users/(?P<fb_username>[-\w]+)/questionnaire/categories/$', 'freyalove.api.views.questionnaire.categories'),
    url(r'^users/(?P<fb_username>[-\w]+)/questionnaire/questions/random/(?P<status>[-\w]+)/$','freyalove.api.views.questionnaire.random_questions'),
    url(r'^users/(?P<fb_username>[-\w]+)/questionnaire/(?P<category>[-\w]+)/(?P<status>[-\w]+)/$','freyalove.api.views.questionnaire.filter_questions'),
    url(r'^questionnaire/questions/add/$', 'freyalove.api.views.questionnaire.answer'),

    # Index
    url(r'^$', 'freyalove.views.hello'),
)
