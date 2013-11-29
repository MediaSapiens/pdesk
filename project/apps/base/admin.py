
from django.contrib import admin
from django.contrib.contenttypes import generic

from project.apps.base.models import RedProject, RedVersion, RedTaskStatus, RedTask
from project.apps.base.models import RedUser, RedRole, RedRoleSet, RedTaskJournalEntry
from tagging.models import TaggedItem


class TagInline(generic.GenericTabularInline):
    model = TaggedItem

class RedUserAdmin(admin.ModelAdmin):
    model = RedUser
    list_display = ('id', 'firstname', 'lastname', 'username', 'email', 'hours', 'tags', 'pdesk_user')
    inlines = [TagInline]

class RedRoleAdmin(admin.ModelAdmin):
    model = RedProject
    list_display = ('id', 'title')

class RedRoleSetAdmin(admin.ModelAdmin):
    model = RedProject
    list_display = ('id', 'role', 'project')



class RedProjectAdmin(admin.ModelAdmin):
    model = RedProject
    list_display = ('id', 'title')

class RedVersionAdmin(admin.ModelAdmin):
    model = RedVersion
    list_display = ('id', 'title', 'project')

class RedTaskStatusAdmin(admin.ModelAdmin):
    model = RedProject
    list_display = ('id', 'title')

class RedTaskAdmin(admin.ModelAdmin):
    model = RedTask
    list_display = ('id', 'title', 'project', 'estimated_hours', 'spent_hours', 'author', 'assigned_to', 'version', 'status', 'updated_on')

class RedTaskJournalEntryAdmin(admin.ModelAdmin):
    model = RedTaskJournalEntry
    list_display = ('id', 'task', 'status', 'created_on')


admin.site.register(RedUser, RedUserAdmin)
admin.site.register(RedRole, RedRoleAdmin)
admin.site.register(RedRoleSet, RedRoleSetAdmin)

admin.site.register(RedProject, RedProjectAdmin)
admin.site.register(RedVersion, RedVersionAdmin)
admin.site.register(RedTaskStatus, RedTaskStatusAdmin)
admin.site.register(RedTask, RedTaskAdmin)
admin.site.register(RedTaskJournalEntry, RedTaskJournalEntryAdmin)


