from django.db import models


class RedUser(models.Model):
    
    red_id = models.IntegerField()
    firstname = models.CharField(max_length=500)
    lastname = models.CharField(max_length=500)
    username = models.CharField(max_length=500)
    email = models.EmailField()


    def __unicode__(self):
        return self.username



class RedProject(models.Model):
    

    red_id = models.IntegerField()
    title = models.CharField(max_length=500)


    def __unicode__(self):
        return self.title



class RedTask(models.Model):

    
    red_id = models.IntegerField()
    title = models.CharField(max_length=500)
    project = models.ForeignKey(RedProject)

    author = models.ForeignKey(RedUser, related_name = 'author')
    assigned_to = models.ForeignKey(RedUser, related_name = 'assigned_to', blank=True, null=True)

    estimated_hours = models.CharField(max_length=500, blank=True, null=True)
    spent_hours = models.CharField(max_length=500, blank=True, null=True)


    def __unicode__(self):
        return self.title

