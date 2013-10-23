# Create your views here.
from redmine import Redmine

from django.http import HttpResponse
from project.settings import REDMINE_HOST, REDMINE_USER, REDMINE_PASS
from project.apps.base.models import RedUser, RedProject, RedTask



def update_db(request):

    red_login = Redmine(REDMINE_HOST, username=REDMINE_USER, password=REDMINE_PASS)

    for user in red_login.users:
        usr = RedUser(id=user.id, username=user.login, email=user.mail,
            lastname=user.lastname, firstname=user.firstname)
        usr.save()
        print usr, 'saved'


  
    for project in red_login.projects:

        proj = RedProject(id=project.id, title=project.name)
        proj.save()
        print proj, 'saved'



        for issue in project.issues:

            author = RedUser.objects.get(id=issue.author.id)
            if issue.assigned_to:
                assigned_to = RedUser.objects.get(id=issue.assigned_to.id)               
            else:
                assigned_to = None

            iss = RedTask(id=issue.id, title=issue.subject, project=proj, estimated_hours=issue.estimated_hours,
                author=author, assigned_to=assigned_to)
            iss.save()
            print iss, 'saved'


    return HttpResponse('Done')