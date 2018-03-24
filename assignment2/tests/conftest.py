import pytest
import os

from flaskr import create_app

@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app
