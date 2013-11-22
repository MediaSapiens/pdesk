
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from project.apps.base.models import RedUser



class PdeskUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)        
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)        
        user.save()
        return user



class PdeskUser(AbstractBaseUser):
    person = models.OneToOneField(RedUser, blank=True, null=True)
    username = models.CharField(max_length=254, unique=True)

    objects = PdeskUserManager()

    USERNAME_FIELD = 'username'