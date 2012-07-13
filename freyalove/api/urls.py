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
	url(r'users/(\d+)/profile/summary/$', 'profile_summary'),
    url(r'users/(\d+)/profile/$', 'profile'),
)
