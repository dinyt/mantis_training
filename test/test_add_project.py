from model.project import Project
import random
import string

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    maxlen = max(random.randrange(maxlen), 5)
    return prefix + "".join([random.choice(symbols) for i in range(maxlen)])

def test_add_project_with_db(app, db):
   old_projects = db.get_project_list()
   project = Project(name=random_string('name_', 10))
   app.project.open_projects_page()
   app.project.create(project)
   assert len(app.project.find_successful_message_after_creating_project) > 0
   new_projects = db.get_project_list()
   old_projects.append(project)
   assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

def test_add_project_with_soap(app):
   user = app.config['webadmin']
   old_projects = app.soap.get_all_projects(user["username"], user["password"])
   project = Project(name=random_string('name_', 10))
   app.project.open_projects_page()
   app.project.create(project)
   new_projects = app.soap.get_all_projects(user["username"], user["password"])
   old_projects.append(project)
   assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
