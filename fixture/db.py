import pymysql.cursors
from model.project import Project

class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=name,
                             autocommit=True)

    def destroy(self):
        self.connection.close()

    def get_project_list(self):
        list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select id, name from mantis_project_table")
            for row in cursor:
                (id, name) = row
                list.append(Project(id=str(id), name=name))
        finally:
            cursor.close()

        return list