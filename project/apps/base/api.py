
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.utils import trailing_slash
# from tastypie.authentication import BasicAuthentication
from django.conf.urls import url


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
        cache = SimpleCache(timeout=10)
        # authentication = BasicAuthentication()


    def dehydrate(self, bundle):
            bundle.data['estimated_sum'] = bundle.obj.estimated_sum()
            bundle.data['spent_sum'] = bundle.obj.spent_sum()
            return bundle



class RoleResource(ModelResource):    

    class Meta:
        queryset = RedRole.objects.all()
        resource_name = 'role'
        filtering = {
                    'id': ALL,
                }

        include_resource_uri = False
        cache = SimpleCache(timeout=10)



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
        cache = SimpleCache(timeout=10)


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
        cache = SimpleCache(timeout=10)
        # authentication = BasicAuthentication()


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




class OtherTaskResource(TaskResource):

    class Meta:
        queryset = RedTask.objects.filter(version=None)




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
        cache = SimpleCache(timeout=10)
        # authentication = BasicAuthentication()               


    def dehydrate_project(self, bundle):
        return bundle.obj.project.id   


    def dehydrate(self, bundle):
            bundle.data['estimated_sum'] = bundle.obj.estimated_sum()
            bundle.data['spent_sum'] = bundle.obj.spent_sum()
            return bundle




class ProjectResource(ModelResource):

    # estimated_sum = fields.FloatField(readonly=True)
    # spent_sum = fields.FloatField(readonly=True)
    roleset = fields.ToManyField(RoleSetResource, 'redroleset_set', full=True)
    versions = fields.ToManyField(VersionResource, 'redversion_set', full=True)
    other_tasks = fields.ToManyField(OtherTaskResource, 'redtask_set', full=True)

    class Meta:
        queryset = RedProject.objects.all()
        resource_name = 'project'
        filtering = {
                    'id': ALL,
                    'roleset': ALL_WITH_RELATIONS,
                }
        # always_return_data = True

        include_resource_uri = False
        cache = SimpleCache(timeout=10)
        # authentication = BasicAuthentication()


    def dehydrate(self, bundle):
            bundle.data['estimated_sum'] = bundle.obj.estimated_sum()
            bundle.data['spent_sum'] = bundle.obj.spent_sum()
            return bundle




class TimeResource(Resource):
   
    class Meta:
        
        resource_name = 'time'

        include_resource_uri = False 
        cache = SimpleCache(timeout=10) 
        # authentication = BasicAuthentication() 


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<type_slug>\w[\w/-]*)/(?P<obj_slug>\w[\w/-]*)%s$" \
                % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_time'), name="api_get_time"),
        ]


    def get_time(self, request, **kwargs):

        responce = {}
        if kwargs['obj_slug'] == 'project':        
       
            time = RedProject.objects.get(id=request.GET['id'])

            if kwargs['type_slug'] == 'spent':
                responce = {'spent_sum':time.spent_sum()}        

            elif kwargs['type_slug'] == 'estimate':
                responce = {'estimated_sum':time.estimated_sum()}  


        elif kwargs['obj_slug'] == 'user':

            time = RedUser.objects.get(id=request.GET['id'])

            if kwargs['type_slug'] == 'spent':
                responce = {'spent_sum':time.spent_sum()}                        

            elif kwargs['type_slug'] == 'estimate':
                responce = {'estimated_sum':time.estimated_sum()}         


        elif kwargs['obj_slug'] == 'all':

            time = RedProject.objects.all()

            if kwargs['type_slug'] == 'spent':
                spent_sum = 0.0
                for obj in time:
                    if obj.spent_sum():                
                        spent_sum += obj.spent_sum()
                responce = {'spent_sum':spent_sum}  

                    

            elif kwargs['type_slug'] == 'estimate':
                estimated_sum = 0.0
                for obj in time:
                    if obj.estimated_sum():                
                        estimated_sum += obj.estimated_sum()
                responce = {'estimated_sum':estimated_sum}  


        return self.create_response(request, responce)