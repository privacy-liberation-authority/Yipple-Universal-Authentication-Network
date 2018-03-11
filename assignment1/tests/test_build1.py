import pytest
from flask import url_for, session
import json
import re
import uuid

register_data = {'username': str(uuid.uuid4()), 'password': 'utest'}

class TestApp:
    def test_home(self, client):
        res = client.get(url_for('basic.home'))
        assert res.status_code == 200
        assert b'Welcome' in res.data

    def test_register(self, client):
        res = client.post('/register', data=register_data)
        assert res.status_code == 302
        assert re.search("/login$", res.location)

    def test_login(self, client):
        res = client.post('/login', data=register_data)
        assert 'username' in session

    def test_login_fail(self, client):
        res = client.post('/login', data={'username': 'i_should_not_login', 'password': 'helloworld'})
        assert 'username' not in session

    def test_me_page(self, client):
        res = client.post('/login', data=register_data)
        res = client.get('/users/me')
        assert res.status_code == 200
        assert register_data['username'].encode('utf-8') in res.data
