import datetime
from dateutil.relativedelta import relativedelta


from django.db import models


def user_limit(self, limit, tasks):
    
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0)

    if limit == 'thisweek':  
        monday_of_this_week = today - datetime.timedelta(days=(today.isocalendar()[2] - 1))
        tasks = self.assigned_to.filter(updated_on__gte=monday_of_this_week)                

    elif limit == 'lastweek':              
        monday_of_this_week = today - datetime.timedelta(days=(today.isocalendar()[2] - 1))
        print monday_of_this_week
        monday_of_last_week = monday_of_this_week - datetime.timedelta(days=7)       
        tasks = self.assigned_to.filter(updated_on__gte=monday_of_last_week, updated_on__lt=monday_of_this_week)
  
    elif limit == 'thismonth':
        start_of_this_month = datetime.datetime(now.year, now.month, 1, 0, 0)
        tasks = self.assigned_to.filter(updated_on__gte=start_of_this_month)

    elif limit == 'lastmonth':
        start_of_this_month = datetime.datetime(now.year, now.month, 1, 0, 0) 
        start_of_last_month = start_of_this_month - relativedelta(months=1)
        tasks = self.assigned_to.filter(updated_on__gte=start_of_last_month, updated_on__lt=start_of_this_month)

    return tasks




def project_limit(self, limit, tasks):

    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day, 0, 0)

    if limit == 'thisweek':  
        monday_of_this_week = today - datetime.timedelta(days=(today.isocalendar()[2] - 1))
        tasks = self.redtask_set.filter(updated_on__gte=monday_of_this_week)                

    elif limit == 'lastweek':              
        monday_of_this_week = today - datetime.timedelta(days=(today.isocalendar()[2] - 1))
        monday_of_last_week = monday_of_this_week - datetime.timedelta(days=7)       
        tasks = self.redtask_set.filter(updated_on__gte=monday_of_last_week, updated_on__lt=monday_of_this_week)
  
    elif limit == 'thismonth':
        start_of_this_month = datetime.datetime(now.year, now.month, 1, 0, 0)
        tasks = self.redtask_set.filter(updated_on__gte=start_of_this_month)

    elif limit == 'lastmonth':
        start_of_this_month = datetime.datetime(now.year, now.month, 1, 0, 0) 
        start_of_last_month = start_of_this_month - relativedelta(months=1)
        tasks = self.redtask_set.filter(updated_on__gte=start_of_last_month, updated_on__lt=start_of_this_month)

    return tasks




class RedUser(models.Model):

    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    email = models.EmailField()

    hours = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.username



    def estimated_sum(self, limit=None):

        tasks = []
        if limit:
            tasks = user_limit(self, limit, tasks)
        else:            
            tasks = self.assigned_to.all()

        estimated_sum = 0.0
        for task in tasks:                      
            if task.estimated_hours:                             
                estimated_sum += task.estimated_hours
        return estimated_sum



    def spent_sum(self, limit=None):  
       
        tasks = []           
        if limit:
            tasks = user_limit(self, limit, tasks)
        else:            
            tasks = self.assigned_to.all()

        spent_sum = 0.0
        for task in tasks:
            if task.spent_hours:                
                spent_sum += task.spent_hours
        return spent_sum




class RedRole(models.Model):
        
    title = models.CharField(max_length=500)

    def __unicode__(self):
        return self.title



class RedProject(models.Model):
    
    title = models.CharField(max_length=500)

    def __unicode__(self):
        return self.title


    def estimated_sum(self, limit=None):

        tasks = []
        if limit:
            tasks = user_limit(self, limit, tasks)
        else:            
            tasks = self.redtask_set.all()


        estimated_sum = 0.0
        for task in tasks:                      
            if task.estimated_hours:                             
                estimated_sum += task.estimated_hours
        return estimated_sum


    def spent_sum(self, limit=None):  
       
        tasks = []
        if limit:           
            tasks = user_limit(self, limit, tasks)
        else:            
            tasks = self.redtask_set.all()


        spent_sum = 0.0
        for task in tasks:
            if task.spent_hours:                
                spent_sum += task.spent_hours
        return spent_sum





class RedRoleSet(models.Model):    
    
    users = models.ManyToManyField(RedUser, blank=True, null=True)
    role = models.ForeignKey(RedRole)
    project = models.ForeignKey(RedProject)

    def __unicode__(self):
        return self.role.title

    class Meta:
        unique_together = ('role', 'project')




class RedVersion(models.Model):

    title = models.CharField(max_length=500)
    project = models.ForeignKey(RedProject)

    def __unicode__(self):
        return self.title


    def estimated_sum(self):

        tasks = self.redtask_set.all()
        estimated_sum = 0.0
        for task in tasks:            
            if task.estimated_hours:                
                estimated_sum += task.estimated_hours
        return estimated_sum


    def spent_sum(self):        
        tasks = self.redtask_set.all()
        spent_sum = 0.0
        for task in tasks:
            if task.spent_hours:                
                spent_sum += task.spent_hours
        return spent_sum



class RedTask(models.Model):    

    title = models.CharField(max_length=500)
    project = models.ForeignKey(RedProject)
    version = models.ForeignKey(RedVersion, blank=True, null=True)

    author = models.ForeignKey(RedUser, related_name = 'author')
    assigned_to = models.ForeignKey(RedUser, related_name = 'assigned_to', blank=True, null=True)

    estimated_hours = models.FloatField(blank=True, null=True)
    spent_hours = models.FloatField(blank=True, null=True)

    updated_on = models.DateTimeField()

    def __unicode__(self):
        return self.title


