
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


from project.apps.base.views import update_db

from tastypie.api import Api
from project.apps.base.api import (UserResource, ProjectResource, VersionResource, 
    TaskResource, TimeResource, ActivityResource, TagResourse)

pdesk = Api(api_name='api')
pdesk.register(UserResource())
pdesk.register(ProjectResource())
pdesk.register(VersionResource())
pdesk.register(TaskResource())
pdesk.register(ActivityResource())
pdesk.register(TimeResource())
pdesk.register(TagResourse())

urlpatterns = patterns('',
    # Examples:
    url(r'^update_db/', update_db),
    url(r'^', include(pdesk.urls)),
    url(r'^index/$', 'project.views.index', name='index'),

    url(r'^admin/', include(admin.site.urls)),
)
