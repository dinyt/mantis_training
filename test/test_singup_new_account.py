import string
import random
import time

def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    maxlen = max(random.randrange(maxlen), 5)
    return prefix + "".join([random.choice(symbols) for i in range(maxlen)])

def test_signup_new_account(app):
    username = random_username('user_', 10)
    password = 'test'
    email = username + "@localhost"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    time.sleep(5)
    #app.session.login(username, password)
    #assert app.session.is_logged_in_as(username)
    #app.session.logout()
    assert app.soap.can_login(username, password) == True