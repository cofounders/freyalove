from django.conf.urls.defaults import *
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

# freyalove models
from freyalove.users.models import Profile

# drfw resource declarations
class ProfileResource(ModelResource):
    model = Profile

urlpatterns = patterns('freyalove.api.views',

	# get routes
	url(r'users/init/$', 'init'),
	url(r'users/(\d+)/friends/(\d+)/mutual/$', 'mutual_friends_in_freya'),
	url(r'users/(\d+)/friends/$', 'friends_in_freya'),
	url(r'users/(\d+)/facebookfriends/$', 'fb_friends'),
	url(r'users/(\d+)/profile/summary/$', 'profile_summary'),
    url(r'users/(\d+)/profile/$', 'profile'),
    url(r'activities/sexytimes/$', 'fetch_sexytimes'),

    url(r'/$', 'hello'),
)
