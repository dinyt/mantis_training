from selenium import webdriver
from fixture.session import SessionHelper
from fixture.james import JamesHelper
from fixture.project import ProjectHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper
from fixture.soap import SoapHelper

class Application:

    #def __init__(self, browser, base_url):
    #def __init__(self, browser, config, base_url):
    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        # implicitly_wait - ожидание тех или иных элементов в браузере
        # self.wd.implicitly_wait(3)
        self.session = SessionHelper(self)
        self.james = JamesHelper(self)
        #self.base_url = base_url
        self.config = config
        self.base_url = config['web']['baseUrl']
        self.project = ProjectHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url()
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)