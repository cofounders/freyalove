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

    # OTHER USERS
    url(r'^users/(?P<fb_username>[-\w]+)/profile/summary/$', 'freyalove.api.views.otherusers.profile_summary'),
    url(r'^users/friends/(?P<fb_username>[-\w]+)/mutual/$', 'freyalove.api.views.otherusers.mutual_friends_in_freya'),
    url(r'^users/(?P<fb_username>[-\w]+)/friends/$', 'freyalove.api.views.otherusers.friends_in_freya'),

    # ACTIVITIES
    url(r'^activities/sexytimes/upcoming/$', 'freyalove.api.views.activities.fetch_sexytimes'), 
    url(r'^activities/winks/unreturned/$', 'freyalove.api.views.activities.fetch_winks'),
    url(r'^activities/$', 'freyalove.api.views.activities.fetch_activities'), # winks and sexytimes combined
    url(r'^activities/sexytimes/create/$', 'freyalove.api.views.activities.create_sexytime'), # create SexyTime
    url(r'^activities/sexytimes/(\d+)/rsvp/$', 'freyalove.api.views.activities.rsvp_sexytime'), # rsvp for a SexyTime
    url(r'^activities/sexytimes/(\d+)/notes/add/$', 'freyalove.api.views.activities.update_sexytime_note'),
    url(r'^activities/winks/to/(\d+)/$', 'freyalove.api.views.activities.create_wink'), # send Wink

    # MESSAGES
    url(r'^conversations/unread/$', 'freyalove.api.views.messages.fetch_unread_conversations'),
    url(r'^conversations/$', 'freyalove.api.views.messages.fetch_conversations'), # fetch all conversations
    url(r'^conversations/(\d+)/messages/$', 'freyalove.api.views.messages.fetch_messages'),
    url(r'^conversations/messages/$', 'freyalove.api.views.messages.send_message'), # send Message, a conversation will be created if it doesn't exist

    # STREAM

    # MATCHMAKING

    # QUESTIONAIRE

    # Index
    url(r'^$', 'freyalove.views.hello'),
)
