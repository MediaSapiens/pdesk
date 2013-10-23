
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from project.apps.base.models import RedUser, RedProject, RedTask


class UserResource(ModelResource):
    class Meta:
        queryset = RedUser.objects.all()
        resource_name = 'user'
        filtering = {
                    'id': ALL,
                }

class ProjectResource(ModelResource):

    estimated_sum = fields.FloatField(readonly=True)
    spent_sum = fields.FloatField(readonly=True)


    class Meta:
        queryset = RedProject.objects.all()
        resource_name = 'project'
        filtering = {
                    'id': ALL,
                }

    def dehydrate_estimated_sum(self, bundle):

        tasks = bundle.obj.redtask_set.all()
        estimated_sum = 0.0
        for task in tasks:            
            if task.estimated_hours:                
                estimated_sum += task.estimated_hours
        return estimated_sum


    def dehydrate_spent_sum(self, bundle):        
        tasks = bundle.obj.redtask_set.all()
        spent_sum = 0.0
        for task in tasks:
            if task.spent_hours:                
                spent_sum += task.spent_hours
        return spent_sum


class TaskResource(ModelResource):

    project = fields.ForeignKey(ProjectResource, 'project')
    author = fields.ForeignKey(UserResource, 'author')
    assigned_to = fields.ForeignKey(UserResource, 'assigned_to', null=True, blank=True)

    class Meta:
        queryset = RedTask.objects.all()
        resource_name = 'task'
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'author': ALL_WITH_RELATIONS, 
            'assigned_to': ALL_WITH_RELATIONS,             
        }

    def dehydrate_project(self, bundle):
        return bundle.obj.project.id      

    def dehydrate_author(self, bundle):
        return bundle.obj.author.id   

    def dehydrate_assigned_to(self, bundle):
        if bundle.obj.assigned_to:
            return bundle.obj.assigned_to.id  
        else:
            return None                 