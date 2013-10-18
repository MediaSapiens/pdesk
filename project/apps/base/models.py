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
        return self.username



class RedTask(models.Model):

    
    red_id = models.IntegerField()
    title = models.CharField(max_length=500)
    project = models.ForeignKey(RedProject)

    estimated_hours = models.CharField(max_length=500)
    spent_hours = models.CharField(max_length=500)


    def __unicode__(self):
        return self.title

