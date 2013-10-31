from django.db import models



class RedUser(models.Model):

    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    email = models.EmailField()

    hours = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.username



class RedRole(models.Model):
        
    title = models.CharField(max_length=500)

    def __unicode__(self):
        return self.title



class RedProject(models.Model):
    
    title = models.CharField(max_length=500)

    def __unicode__(self):
        return self.title



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



class RedTask(models.Model):    

    title = models.CharField(max_length=500)
    project = models.ForeignKey(RedProject)
    version = models.ForeignKey(RedVersion, blank=True, null=True)

    author = models.ForeignKey(RedUser, related_name = 'author')
    assigned_to = models.ForeignKey(RedUser, related_name = 'assigned_to', blank=True, null=True)

    estimated_hours = models.FloatField(blank=True, null=True)
    spent_hours = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.title


