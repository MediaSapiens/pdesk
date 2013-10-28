
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


from project.apps.base.views import update_db

from tastypie.api import Api
from project.apps.base.api import UserResource, ProjectResource, TaskResource


v1_api = Api(api_name='api')
v1_api.register(UserResource())
v1_api.register(ProjectResource())
v1_api.register(TaskResource())


urlpatterns = patterns('',
    # Examples:
    url(r'^update_db/', update_db),
    url(r'^', include(v1_api.urls)),
    url(r'^index/$', 'project.views.index', name='index'),

    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
