# Create your views here.
from redmine import Redmine

from django.http import HttpResponse
from project.settings import REDMINE_HOST, REDMINE_USER, REDMINE_PASS
from project.apps.base.models import RedProject, RedVersion, RedTaskStatus, RedTask
from project.apps.base.models import RedUser, RedRole, RedRoleSet, RedTaskJournalEntry


def update_db(request):

    red_login = Redmine(REDMINE_HOST, username=REDMINE_USER, password=REDMINE_PASS)
    
# Fetch Users

    for user in red_login.users:
        usr = RedUser(id=user.id, username=user.login, email=user.mail,
            lastname=user.lastname, firstname=user.firstname)
        usr.save()


# Fetch Roles

    for role in red_login.roles:
        rle = RedRole(id=role.id, title=role.name)
        rle.save()


# Fetch Task statuses

    for status in red_login.issue_statuses:
        sts = RedTaskStatus(id=status.id, title=status.name)
        sts.save()


# Fetch Projects

    for project in red_login.projects:

        proj = RedProject(id=project.id, title=project.name)
        proj.save()
        print proj, 'saved'


    # Fetch members of project
 
        for member in project.members:      

            m_user = RedUser.objects.get(id=member.user.id)
            m_role = RedRole.objects.get(id=member.roles[0]['id'])

            try:
                rlse = RedRoleSet.objects.get(role=m_role, project=proj)
                rlse.users.add(m_user)
                rlse.save()

            except RedRoleSet.DoesNotExist:
                rlse = RedRoleSet(role=m_role, project=proj)
                rlse.save()    
                rlse.users.add(m_user)
                rlse.save()          



    # Fetch roadmaps of project

        for version in project.versions:

            ver = RedVersion(id=version.id, title=version.name, project=proj)
            ver.save()
          


    # Fetch tasks of project

        for issue in project.issues:

            author = RedUser.objects.get(id=issue.author.id)
            status = RedTaskStatus.objects.get(id=issue.status.id)

            if issue.assigned_to:
                assigned_to = RedUser.objects.get(id=issue.assigned_to.id)               
            else:
                assigned_to = None

            if issue.fixed_version:
                fixed_version = RedVersion.objects.get(id=issue.fixed_version.id)               
            else:
                fixed_version = None

            iss = RedTask(id=issue.id, title=issue.subject, project=proj, estimated_hours=issue.estimated_hours, 
                spent_hours=issue.get_spent_hours(), author=author, assigned_to=assigned_to, 
                version=fixed_version, updated_on=issue.updated_on, status=status)
            iss.save()
            print iss, 'saved'

            if issue.journals:
                for journal in issue.journals:
                    for detail in journal.details:
                        if detail['name'] == 'status_id':
                            status = RedTaskStatus.objects.get(id=int(detail['new_value']))
                            user = RedUser.objects.get(id=journal.user)
                            jrn = RedTaskJournalEntry(id=journal.id, task=iss, status=status, 
                                user=user, created_on=journal.created_on)
                            jrn.save()
                           
    return HttpResponse('Done')


"""

"journals":[
{"details":[{"name":"status_id","property":"attr","new_value":"2","old_value":"1"},
{"name":"assigned_to_id","property":"attr","new_value":"1"},
{"name":"done_ratio","property":"attr","new_value":"10","old_value":"0"}
,{"name":"estimated_hours","property":"attr","new_value":"1"}],
"created_on":"2013-11-07T12:50:18Z","id":5,"user":{"name":"Mikhail Kushchenko","id":3},"notes":""}]


"journals":[
    {"details":
    [{"name":"1","property":"attachment","new_value":"((.png"},
    {"name":"status_id","property":"attr","new_value":"3","old_value":"2"},
    {"name":"assigned_to_id","property":"attr","new_value":"1","old_value":"3"}],
    "created_on":"2013-11-06T11:16:59Z","id":3,"user":{"name":"Mikhail Kushchenko","id":3},"notes":"dsfdfsdfs"},

    {"details":
    [{"name":"status_id","property":"attr","new_value":"6","old_value":"3"},
    {"name":"assigned_to_id","property":"attr","new_value":"4","old_value":"1"},
    {"name":"done_ratio","property":"attr","new_value":"30","old_value":"0"}],
    "created_on":"2013-11-06T11:18:58Z","id":4,"user":{"name":"Mikhail Kushchenko","id":3},"notes":"g"}
    ],

"""   