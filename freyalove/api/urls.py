from django.conf.urls.defaults import *

urlpatterns = patterns('freyalove.api.views',  
    url(r'profile/(\d+)/$', 'profile'),
)
