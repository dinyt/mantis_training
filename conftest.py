from fixture.application import Application
from fixture.db import DbFixture
import pytest
import json
import os.path
import ftputil

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file_path) as config_file:
            target = json.load(config_file)
    return target


@pytest.fixture(scope="session")
def app(request, config):
    global fixture

    browser = request.config.getoption("--browser")

    #web_config = load_config(request.config.getoption("--target"))["web"]

    if fixture is None or not fixture.is_valid():
        #fixture = Application(browser=browser, base_url=web_config["baseUrl"])
        #fixture = Application(browser=browser, base_url=config["web"]["baseUrl"])
        #fixture = Application(browser=browser, config=config, base_url=web_config["baseUrl"])
        fixture = Application(browser=browser, config=config)

    fixture.session.ensure_login(username=config['webadmin']["username"], password=config['webadmin']["password"])
    #fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture

# scope - выполнение тестов в одной сессии (в самом начале выполнения автотестов)
# autouse - срабатывание фикстуры автоматически
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            remote.remove("config_defaults_inc.php.bak")
        if remote.path.isfile("config_defaults_inc.php"):
            remote.rename("config_defaults_inc.php", "config_defaults_inc.php.bak")
        # почему-то в качестве каталога на удалённом сервере используется тот, в котором находится
        # файл conftest.py
        #remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_defaults_inc.php"),
        #              "config_defaults_inc.php")
        # поэтому, для того чтобы отработал код - использую абсолютные пути
        remote.upload("C://xampp//htdocs//mantisbt-2.25.0//resources//config_defaults_inc.php",
                      "config_defaults_inc.php")

@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.php.bak"):
            if remote.path.isfile("config_defaults_inc.php"):
                remote.remove("config_defaults_inc.php")
            remote.rename("config_defaults_inc.php.bak", "config_defaults_inc.php")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    dbfixture = DbFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"],
                          password=db_config["password"])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture