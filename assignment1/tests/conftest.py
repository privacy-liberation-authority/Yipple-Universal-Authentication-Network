import pytest
import os

from flaskr import create_app

user_folder = os.path.dirname(__file__) + "/../"
user_orig = user_folder + "user.json"
user_back = user_folder + "user.json.back"

def pytest_sessionstart(session):
    ''' Backup original config file'''
    if os.path.isfile(user_orig):
        os.rename(user_orig, user_back)

def pytest_sessionfinish(session, exitstatus):
    ''' And vice versa '''
    if os.path.isfile(user_back):
        os.rename(user_back, user_orig)

@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app
