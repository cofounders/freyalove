from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Django Admin urls
    url(r'^nimdatux/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    # API urls
    # get routes
    url(r'^users/init/$', 'freyalove.api.views.init'),
    url(r'^users/friends/(?P<fb_username>[-\w]+)/mutual/$', 'freyalove.api.views.mutual_friends_in_freya'),
    url(r'^users/(\d+)/friends/$', 'freyalove.api.views.friends_in_freya'),
    url(r'^users/(\d+)/facebookfriends/$', 'freyalove.api.views.fb_friends'),
    url(r'^users/(?P<fb_username>[-\w]+)/profile/summary/$', 'freyalove.api.get_user_summary'),
    url(r'^profile/summary/$', 'freyalove.api.views.profile_summary'),
    url(r'^profile/details/$', 'freyalove.api.views.profile_details'),
    url(r'^profile/unregister/$', 'freyalove.api.views.profile_unregister'),
    url(r'^profile/$', 'freyalove.api.views.profile'), # POST/GET 2-in-1
    url(r'^users/search/$', 'freyalove.api.views.search'), 
    url(r'^activities/sexytimes/upcoming/$', 'freyalove.api.views.fetch_sexytimes'), 
    url(r'^activities/winks/unreturned/$', 'freyalove.api.views.fetch_winks'),
    url(r'^activities/$', 'freyalove.api.views.fetch_activities'), # winks and sexytimes combined
    url(r'^conversations/unread/$', 'freyalove.api.views.fetch_unread_conversations'),
    url(r'^conversations/$', 'freyalove.api.views.fetch_conversations'), # fetch all conversations
    url(r'^conversations/(\d+)/messages/$', 'freyalove.api.views.fetch_messages'),
    
    # post routes
    url(r'^activities/sexytimes/create/$', 'freyalove.api.views.create_sexytime'), # create SexyTime
    url(r'^activities/sexytimes/(\d+)/rsvp/$', 'freyalove.api.views.rsvp_sexytime'), # rsvp for a SexyTime
    url(r'^activities/sexytimes/(\d+)/notes/add/$', 'freyalove.api.views.update_sexytime_note'),
    url(r'^activities/winks/to/(\d+)/$', 'freyalove.api.views.create_wink'), # send Wink
    url(r'^conversations/messages/$', 'freyalove.api.views.send_message'), # send Message, a conversation will be created if it doesn't exist

    # Index
    url(r'^$', 'freyalove.api.views.hello'),
)
