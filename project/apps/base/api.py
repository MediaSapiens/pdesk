
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from project.apps.base.models import RedUser, RedProject, RedTask


class UserResource(ModelResource):
    class Meta:
        queryset = RedUser.objects.all()
        resource_name = 'user'


class ProjectResource(ModelResource):
    class Meta:
        queryset = RedProject.objects.all()
        resource_name = 'project'
        filtering = {
                    'id': ALL,
                }


class TaskResource(ModelResource):

    project = fields.ForeignKey(ProjectResource, 'project')

    class Meta:
        queryset = RedTask.objects.all()
        resource_name = 'task'
        filtering = {
            'project': ALL_WITH_RELATIONS,            
        }