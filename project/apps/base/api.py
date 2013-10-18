
from tastypie.resources import ModelResource
from project.apps.base.models import RedUser, RedProject


class UserResource(ModelResource):
    class Meta:
        queryset = RedUser.objects.all()
        resource_name = 'user'


class ProjectResource(ModelResource):
    class Meta:
        queryset = RedProject.objects.all()
        resource_name = 'project'


