
from django.contrib import admin

from project.apps.base.models import RedUser, RedProject, RedTask


class RedUserAdmin(admin.ModelAdmin):
    model = RedUser
    list_display = ('red_id', 'firstname', 'lastname', 'username', 'email')



class RedProjectAdmin(admin.ModelAdmin):
    model = RedProject
    list_display = ('red_id', 'title')


class RedTaskAdmin(admin.ModelAdmin):
    model = RedTask
    list_display = ('red_id', 'title', 'project', 'estimated_hours', 'spent_hours')



admin.site.register(RedUser, RedUserAdmin)
admin.site.register(RedProject, RedProjectAdmin)
admin.site.register(RedTask, RedTaskAdmin)