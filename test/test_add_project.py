from model.project import Project
import random
import string

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_add_project(app, db):
    old_projects = db.get_project_list()
    project = Project(name=random_string('name_', 10))
    app.project.open_projects_page()
    app.project.create(project)
    assert len(app.project.find_successful_message_after_creating_project) > 0
    new_projects = db.get_project_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)