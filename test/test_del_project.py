from model.project import Project
import random

def test_delete_some_project_with_db(app, db):
    if db.get_project_list() == 0:
        app.project.create(Project(name="New project"))
    old_projects = db.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_by_id(project.id)
    new_projects = db.get_project_list()
    assert len(old_projects) - 1 == app.project.count()
    old_projects.remove(project)
    assert old_projects == new_projects
    assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)

def test_delete_some_project_with_soap(app):
    user = app.config['webadmin']
    old_projects = app.soap.get_all_projects(user["username"], user["password"])
    if old_projects == 0:
        app.project.create(Project(name="New project"))
        old_projects = app.soap.get_all_projects(user["username"], user["password"])
    project = random.choice(old_projects)
    app.project.delete_by_id(project.id)
    new_projects = app.soap.get_all_projects(user["username"], user["password"])
    assert len(old_projects) - 1 == app.project.count()
    old_projects.remove(project)
    assert old_projects == new_projects
    assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)