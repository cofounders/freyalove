from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'freyalove.views.home', name='home'),
    # url(r'^freyalove/', include('freyalove.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^nimdatux/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),

    # App urls
    url(r'^api/', include('freyalove.api.urls')),
    
    # Other pages
    #url(r'^$', 'freyalove.views.homepage'),
)
