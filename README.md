====
Plandesk.io project
====

API

http://127.0.0.1:8000/api/ api overview

1 )users

http://127.0.0.1:8000/api/user/     get all users
http://127.0.0.1:8000/api/user/1/  get user with id 1


http://127.0.0.1:8000/api/user/?tags__name=CSS get users with tag CSS
http://127.0.0.1:8000/api/user/?tags__id=1 get users with tag id 1

http://127.0.0.1:8000/api/tag/ get all tags
http://127.0.0.1:8000/api/tag/1/  get tag with id 1


responce:
{
"id": 1, 
"email": "sfelde@mediasapiens.co", 
"firstname": "Sergej", 
"lastname": "Felde", 
"username": "sfelde"
"hours": null, 
}


2 )projects

http://127.0.0.1:8000/api/project/    get all projects
http://127.0.0.1:8000/api/project/2/ get project with id 2

responce:
{
"estimated_sum": 14.0,  
"id": 2,  
"roleset": [
    {
        "id": 6,  
        "role": "Developer",  
        "users": [{
                "email": "petr@petr.com",  
                "firstname": "petr",  
                "hours": null,  
                "id": 4,  
                "lastname": "petr",
                 "username": "petr"
            }]
    },
     {
        "id": 7,  
        "role": "Manager",
         "users": [{
                "email": "mikhail.kushchenko@mediasapiens.co",  
                "firstname": "Mikhail",  
                "hours": null,  
                "id": 3,  
                "lastname": "Kushchenko",  
                "username": "mikhail.kushchenko"
            }, {
                "email": "sfelde@mediasapiens.co",  
                "firstname": "Sergej",  
                "hours": null,
                 "id": 1,  
                "lastname": "Felde",  
                "username": "sfelde"
            }]
    }],  
"spent_sum": 6.0,  
"title": "plandesk",  
"versions": [
    {
        "id": 1,  
        "tasks": [{
            "assigned_to": null,
             "author": 3,  
            "estimated_hours": 4.0,  
            "id": 5,  
            "spent_hours": 0.0,  
            "title": "??"
        }, {
            "assigned_to": null,  
            "author": 3,
             "estimated_hours": 4.0,
             "id": 6,  
            "spent_hours": 2.0,
             "title": "hhhh"
        }],  
        "title": "2"}]
}



http://127.0.0.1:8000/api/task/ get all tasks
http://127.0.0.1:8000/api/task/4/ get  task with id 4

responce:
{
"assigned_to": 3,
 "author": 3, 
"estimated_hours": "1.0", 
"spent_hours": null, 
"id": 4, 
"project": 2, 
"title": "j"
}


http://127.0.0.1:8000/api/task/set/1;3;4/ get tasks with id 1;3;4
http://127.0.0.1:8000/api/task/?project__id=6  get tasks for project with id 6
http://127.0.0.1:8000/api/task/?assigned_to__id=3 get tasks assigned to user with id 3


3 )roadmaps

http://127.0.0.1:8000/api/version/ get all roadmaps
http://127.0.0.1:8000/api/version/1/ get roadmap with id 1
http://127.0.0.1:8000/api/version/?project__id=2  get roadmaps for project with id 2
http://127.0.0.1:8000/api/task/?version__id=1 get tasks for roadmap with id 1



4) activity

http://127.0.0.1:8000/api/activity/?type=all  get all activity
http://127.0.0.1:8000/api/activity/?type=project;id=2 get activity for project with id 2
http://127.0.0.1:8000/api/activity/?type=user;id=3  get activity for user with id 3

pagination
http://127.0.0.1:8000/api/activity/?limit=2&type=all&offset=40    get next 20 items


 5) time spent/estimates

http://127.0.0.1:8000/api/time/estimate/all/ get estimate sum for all redmine
http://127.0.0.1:8000/api/time/spent/all/ get spent time sum for all redmine

http://127.0.0.1:8000/api/time/spent/all/?timelimit=thisweek  get spent sum for all projects limit by this week
http://127.0.0.1:8000/api/time/spent/all/?timelimit=lastweek get spent sum for all projects limit by last week
http://127.0.0.1:8000/api/time/estimate/all/?timelimit=thismonth  get estimate sum for all projects limit by this month
http://127.0.0.1:8000/api/time/estimate/all/?timelimit=lastmonth  get estimate sum for all projects limit by last month


http://127.0.0.1:8000/api/time/estimate/user/?id=4 get estimate sum for user with id 4
http://127.0.0.1:8000/api/time/spent/project/?id=4 get spent sum for project with id 4
http://127.0.0.1:8000/api/time/spent/project/?id=1;timelimit=thisweek get spent sum for project with id 1 limit by this week
http://127.0.0.1:8000/api/time/spent/user/?id=1;timelimit=lastweek get spent sum for user with id 1 limit by last week  
