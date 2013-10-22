
from tastypie.resources import ModelResource
from project.apps.base.models import RedUser, RedProject, RedTask


class UserResource(ModelResource):
    class Meta:
        queryset = RedUser.objects.all()
        resource_name = 'user'


class ProjectResource(ModelResource):
    class Meta:
        queryset = RedProject.objects.all()
        resource_name = 'project'


class TaskResource(ModelResource):
    class Meta:
        queryset = RedTask.objects.all()
        resource_name = 'task'