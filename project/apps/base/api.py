
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.utils import trailing_slash
# from tastypie.cache import SimpleCache,
from tastypie.authentication import BasicAuthentication
from django.conf.urls import url

from tagging.models import Tag
from project.apps.base.models import RedProject, RedVersion, RedTask
from project.apps.base.models import RedUser, RedRole, RedRoleSet, RedTaskJournalEntry


class TagResourse(ModelResource):

    # users = fields.CharField()

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        filtering = {
                    'name': ALL, 
                    'id': ALL,
                }
        include_resource_uri = False
        # cache = SimpleCache(timeout=10)
        authentication = BasicAuthentication()


class UserResource(ModelResource):

    tag = fields.ToManyField(TagResourse, 'tags', null=True, blank=True)

    class Meta:
        queryset = RedUser.objects.all()
        resource_name = 'user'
        filtering = {
                    'id': ALL,
                    'tags': ALL_WITH_RELATIONS,
                }
        include_resource_uri = False
        # cache = SimpleCache(timeout=10)
        authentication = BasicAuthentication()

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
        # cache = SimpleCache(timeout=10)



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
        # cache = SimpleCache(timeout=10)

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
        # cache = SimpleCache(timeout=10)
        authentication = BasicAuthentication()


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
        # cache = SimpleCache(timeout=10)
        authentication = BasicAuthentication()               

    def dehydrate_project(self, bundle):
        return bundle.obj.project.id   

    def dehydrate(self, bundle):
            bundle.data['estimated_sum'] = bundle.obj.estimated_sum()
            bundle.data['spent_sum'] = bundle.obj.spent_sum()
            return bundle




class ProjectResource(ModelResource):

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
        include_resource_uri = False
        # cache = SimpleCache(timeout=10)
        authentication = BasicAuthentication()

    def dehydrate(self, bundle):
            bundle.data['estimated_sum'] = bundle.obj.estimated_sum()
            bundle.data['spent_sum'] = bundle.obj.spent_sum()
            return bundle




class ActivityResource(Resource):
   
    class Meta:
        resource_name = 'activity'
        include_resource_uri = False
        max_limit = 20 
        # cache = SimpleCache(timeout=10) 
        authentication = BasicAuthentication() 


    def obj_get_list(self, bundle, **kwargs):

        responce = []
        tasks = []
        projects = []

        if bundle.request.user.is_superuser:    
            user_perm = False            
        else:
            try:
                user_perm = bundle.request.user.reduser                
                rolesets = RedRoleSet.objects.filter(users=user_perm)
                for role in rolesets:
                    projects.append(role.project)                
            except RedUser.DoesNotExist:
                user_perm = False


        if bundle.request.GET['type'] == 'all':
            if user_perm:                
                tasks = RedTask.objects.filter(project__in=projects)
            else:
                tasks = RedTask.objects.all()


        elif bundle.request.GET['type'] == 'project':
            try:
                project = RedProject.objects.get(id=bundle.request.GET['id'])
                if user_perm:                    
                    if project in projects:
                        tasks = RedTask.objects.filter(project=project)
                    else:
                        tasks = False
                else:
                    tasks = RedTask.objects.filter(project=project)                    
            except RedProject.DoesNotExist:
                pass


        if tasks:
            for task in tasks:
                if task.redtaskjournalentry_set.all():
                    for journal in task.redtaskjournalentry_set.all():
                        journal_dict = { 'user': journal.user,
                                          'task': task,
                                          'status': journal.status,
                                          'date': journal.created_on }
                        responce.append(journal_dict)

                else:
                    journal_dict = { 'user': task.author,
                                      'task': task,
                                      'status': task.status,
                                      'date': task.updated_on }
                    responce.append(journal_dict) 


        elif bundle.request.GET['type'] == 'user':
            try:
                user = RedUser.objects.get(id=bundle.request.GET['id'])
                authors = RedTask.objects.filter(author=user)
                for task in authors:
                    journal_dict = { 'user': task.author,
                                      'task': task,
                                      'status': task.status,
                                      'date': task.updated_on }
                    responce.append(journal_dict)

                others = RedTaskJournalEntry.objects.filter(user=user)
                for journal in others:
                    journal_dict = { 'user': journal.user,
                                      'task': journal.task,
                                      'status': journal.status,
                                      'date': journal.created_on }
                    responce.append(journal_dict)

            except RedUser.DoesNotExist:
                pass

        responce = sorted(responce, key=lambda k: k['date'], reverse=True) 
        return responce


    def dehydrate(self, bundle):
            bundle.data['user'] = bundle.obj['user']
            bundle.data['task'] = bundle.obj['task']
            bundle.data['status'] = bundle.obj['status']
            bundle.data['date'] = bundle.obj['date']
            return bundle




class TimeResource(Resource):
   
    class Meta:
        
        resource_name = 'time'
        include_resource_uri = False 
        # cache = SimpleCache(timeout=10) 
        authentication = BasicAuthentication() 

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<type_slug>\w[\w/-]*)/(?P<obj_slug>\w[\w/-]*)%s$" \
                % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_time'), name="api_get_time"),
        ]

    def get_time(self, request, **kwargs):

        responce = {}
        time = None

        if kwargs['obj_slug'] == 'project':

            try:       
                time = RedProject.objects.get(id=request.GET['id'])
            except RedProject.DoesNotExist:
                pass

        elif kwargs['obj_slug'] == 'user':

            try:
                time = RedUser.objects.get(id=request.GET['id'])
            except RedUser.DoesNotExist:
                pass


        if time:
            if kwargs['type_slug'] == 'spent':
                if 'timelimit' in request.GET:
                    responce = {'spent_sum':time.spent_sum(limit=request.GET['timelimit'])}  
                else:
                    responce = {'spent_sum':time.spent_sum()}                     

            elif kwargs['type_slug'] == 'estimate':
                if 'timelimit' in request.GET:
                    responce = {'estimated_sum':time.estimated_sum(limit=request.GET['timelimit'])}  
                else:
                    responce = {'estimated_sum':time.estimated_sum()}  


        elif kwargs['obj_slug'] == 'all':
            print '---->all<----'

            time = RedProject.objects.all()   

            if kwargs['type_slug'] == 'spent':                
                spent_sum = 0.0
                for obj in time:
                    if 'timelimit' in request.GET:                              
                        if obj.spent_sum(limit=request.GET['timelimit']):              
                            spent_sum += obj.spent_sum(limit=request.GET['timelimit'])                            
                    else: 
                        if obj.spent_sum():                                         
                            spent_sum += obj.spent_sum()
                responce = {'spent_sum':spent_sum}            

            elif kwargs['type_slug'] == 'estimate':
                estimated_sum = 0.0
                for obj in time:
                    if 'timelimit' in request.GET:                              
                        if obj.estimated_sum(limit=request.GET['timelimit']):              
                            estimated_sum += obj.estimated_sum(limit=request.GET['timelimit'])                            
                    else: 
                        if obj.estimated_sum():
                            estimated_sum += obj.estimated_sum()
                responce = {'estimated_sum':estimated_sum}  


        return self.create_response(request, responce)