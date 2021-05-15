

def test_login(app):
    app.open_home_page()
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")