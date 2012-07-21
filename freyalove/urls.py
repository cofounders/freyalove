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
    url(r'^users/(\d+)/friends/(\d+)/mutual/$', 'freyalove.api.views.mutual_friends_in_freya'),
    url(r'^users/(\d+)/friends/$', 'freyalove.api.views.friends_in_freya'),
    url(r'^users/(\d+)/facebookfriends/$', 'freyalove.api.views.fb_friends'),
    url(r'^users/(\d+)/profile/summary/$', 'freyalove.api.views.profile_summary'),
    url(r'^users/(\d+)/profile/$', 'freyalove.api.views.profile'), # POST/GET 2-in-1
    url(r'^activities/sexytimes/$', 'freyalove.api.views.fetch_sexytimes'), 
    url(r'^activities/winks/$', 'freyalove.api.views.fetch_winks'),

    # post routes
    url(r'^activities/sexytimes/create/$', 'freyalove.api.views.create_sexytime'), # create SexyTime
    url(r'^activities/sexytimes/(\d+)/rsvp/$', 'freyalove.api.views.rsvp_sexytime'), # rsvp for a SexyTime
    url(r'^activities/sexytimes/(\d+)/notes/$', 'freyalove.api.views.update_sexytime_note'),
    url(r'^activities/winks/from/(\d+)/to/(\d+)/$', 'freyalove.api.views.create_wink'),

    # Index
    url(r'^$', 'freyalove.api.views.hello'),
)
