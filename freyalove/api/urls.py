from django.conf.urls.defaults import *
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

# freyalove models
from freyalove.users.models import Profile

# drfw resource declarations
class ProfileResource(ModelResource):
    model = Profile

urlpatterns = patterns('freyalove.api.views',  
	# drfw doodles
	url(r'profile/drfw/$', ListOrCreateModelView.as_view(resource=ProfileResource)),
    url(r'profile/drfw/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=ProfileResource)),
	# kenny doodles
    url(r'profile/(\d+)/$', 'profile'),
)
