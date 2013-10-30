
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields

from project.apps.base.models import RedProject, RedVersion, RedTask
from project.apps.base.models import RedUser, RedRole, RedRoleSet


class UserResource(ModelResource):
    class Meta:
        queryset = RedUser.objects.all()
        resource_name = 'user'
        filtering = {
                    'id': ALL,
                }
        include_resource_uri = False



class RoleResource(ModelResource):    

    class Meta:
        queryset = RedRole.objects.all()
        resource_name = 'role'
        filtering = {
                    'id': ALL,
                }
        include_resource_uri = False



class RoleSetResource(ModelResource):

    role = fields.ForeignKey(RoleResource, 'role')
    users = fields.ToManyField(UserResource, 'users', full=True)

    class Meta:
        queryset = RedRoleSet.objects.all()
        resource_name = 'roleset'
        filtering = {
                    'id': ALL,
                    'role': ALL_WITH_RELATIONS,
                }
        include_resource_uri = False   


    def dehydrate_role(self, bundle):
        return bundle.obj.role.title  




class TaskResource(ModelResource):

    project = fields.ForeignKey( 'project.apps.base.api.ProjectResource', 'project')
    version = fields.ForeignKey('project.apps.base.api.VersionResource', 'version', null=True, blank=True)
    author = fields.ForeignKey(UserResource, 'author')
    assigned_to = fields.ForeignKey(UserResource, 'assigned_to', null=True, blank=True)

    class Meta:
        queryset = RedTask.objects.all()
        resource_name = 'task'
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'version': ALL_WITH_RELATIONS,
            'author': ALL_WITH_RELATIONS, 
            'assigned_to': ALL_WITH_RELATIONS,             
        }
        include_resource_uri = False


    def dehydrate_project(self, bundle):
        return bundle.obj.project.id      

    def dehydrate_version(self, bundle):
        if bundle.obj.version:
            return bundle.obj.version.id   
        else:
            return None

    def dehydrate_author(self, bundle):
        return bundle.obj.author.id   

    def dehydrate_assigned_to(self, bundle):
        if bundle.obj.assigned_to:
            return bundle.obj.assigned_to.id  
        else:
            return None 



class VersionResource(ModelResource):

    estimated_sum = fields.FloatField(readonly=True)
    spent_sum = fields.FloatField(readonly=True)
    project = fields.ForeignKey('project.apps.base.api.ProjectResource', 'project')
    tasks = fields.ToManyField(TaskResource, 'redtask_set', full=True)
    
    class Meta:
        queryset = RedVersion.objects.all()
        resource_name = 'version'
        filtering = {
                    'id': ALL,
                    'project': ALL_WITH_RELATIONS,
                    'tasks': ALL_WITH_RELATIONS,

                }
        include_resource_uri = False                


    def dehydrate_project(self, bundle):
        return bundle.obj.project.id   


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



class ProjectResource(ModelResource):

    estimated_sum = fields.FloatField(readonly=True)
    spent_sum = fields.FloatField(readonly=True)
    roleset = fields.ToManyField(RoleSetResource, 'redroleset_set', full=True)
    versions = fields.ToManyField(VersionResource, 'redversion_set', full=True)
    # other_tasks = fields.ToManyField(TaskResource, 'redtask_set', full=True)

    class Meta:
        queryset = RedProject.objects.all()
        resource_name = 'project'
        filtering = {
                    'id': ALL,
                    'roleset': ALL_WITH_RELATIONS,
                }
        # always_return_data = True
        include_resource_uri = False



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

  
    # def dehydrate_other_tasks(self, bundle):        

    #     print bundle.data
    #     print dir(bundle)

    #     return None


                