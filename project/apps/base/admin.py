
from django.contrib import admin

from project.apps.base.models import RedUser, RedProject, RedTask


class RedUserAdmin(admin.ModelAdmin):
    model = RedUser
    list_display = ('id', 'firstname', 'lastname', 'username', 'email')



class RedProjectAdmin(admin.ModelAdmin):
    model = RedProject
    list_display = ('id', 'title')


class RedTaskAdmin(admin.ModelAdmin):
    model = RedTask
    list_display = ('id', 'title', 'project', 'estimated_hours', 'spent_hours', 'author', 'assigned_to')



admin.site.register(RedUser, RedUserAdmin)
admin.site.register(RedProject, RedProjectAdmin)
admin.site.register(RedTask, RedTaskAdmin)