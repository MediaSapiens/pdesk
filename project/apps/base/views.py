# Create your views here.

from django.http import HttpResponse
from project.settings import REDMINE_HOST, REDMINE_USER, REDMINE_PASS

from redmine import Redmine

def update_db(request):

    red_login = Redmine(REDMINE_HOST, username=REDMINE_USER, password=REDMINE_PASS)

    for project in red_login.projects:
        print project

    return HttpResponse('Done')