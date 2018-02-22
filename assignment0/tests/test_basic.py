# test_app.py
import pytest
from flask import url_for


class TestApp:
    def test_home(self, client):
        res = client.get(url_for('basic.home'))
        assert res.status_code == 200
        assert b'Welcome to my testing app' in res.data
