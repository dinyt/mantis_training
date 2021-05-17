from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-2.25.0/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_all_projects(self, username, password):
        client = Client("http://localhost/mantisbt-2.25.0/api/soap/mantisconnect.php?wsdl")
        list = []
        try:
            res = client.service.mc_projects_get_user_accessible(username, password)
            for item in res:
                list.append(Project(id=str(item.id), name=item.name))
            return list
        except WebFault:
            return list