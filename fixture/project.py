class ProjectHelper():
    
    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        # открыть страницу "Управление"
        wd.find_element_by_xpath('//a[@href = "/mantisbt-2.25.0/manage_overview_page.php"]').click()
        # открыть вкладку "Управление проектами"
        wd.find_element_by_xpath('//a[@href = "/mantisbt-2.25.0/manage_proj_page.php"]').click()

    def fill_form_project(self, project):
        wd = self.app.wd
        wd.find_element_by_id("project-name").clear()
        wd.find_element_by_id("project-name").send_keys(project.name)

    def create(self, project):
        wd = self.app.wd
        # нажать на кнопку "Создать новый проект"
        wd.find_element_by_xpath('//button[@class="btn btn-primary btn-white btn-round"]').click()
        # заполнение полей проекта
        self.fill_form_project(project)
        # сохранение проекта
        wd.find_element_by_xpath('//input[@class="btn btn-primary btn-white btn-round"]').click()

    def find_successful_message_after_creating_project(self):
        wd = self.app.wd
        wd.find_element_by_xpath('//div[@class="alert alert-success center"]')

    def count(self):
        wd = self.app.wd
        self.open_projects_page()
        return len(wd.find_elements_by_xpath('//i[@class="fa fa-check fa-lg"]'))

    def delete_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        self.open_project_by_id(id)
        # submit deletion
        wd.find_element_by_xpath('//input[@class="btn btn-primary btn-sm btn-white btn-round"]').click()
        self.set_delete_confirmation()

    def open_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath('//a[@href = "/manage_proj_edit_page.php?project_id=' + str(id) + '"]').click()

    def set_delete_confirmation(self):
        wd = self.app.wd
        wd.find_element_by_xpath('//input[@class="btn btn-primary btn-white btn-round"]').click()