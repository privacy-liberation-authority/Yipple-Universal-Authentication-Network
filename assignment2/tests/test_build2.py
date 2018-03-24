# Configure Two Entires in your database like so. (If you haven't merged initdb.)
#
# 'type': 'admin'
# 'username': 'admin'
# 'password': 'alice'
# 'name': 'Alice Administrator'
# 'address':'Omnipotent'
# 'email':'alice@alice.com'
# 'phonenum':'+313 373 8483'
# 'funds':'31333337'

# 'type': 'user'
# 'username': 'carol'
# 'password': '0xbeefcafebabe'
# 'name': 'Sweet Carolina'
# 'address':'Californ-eye-ay'
# 'email':'carol@candle.lite'
# 'phonenum':'+66 666 6666'
# 'funds':'41424344'

import pytest
from flask import url_for, session
import json
import re
import uuid
import unittest

# Import the app
from flaskr import app

admin_data = {'username': 'admin', 'password': 'alice'}
user_data = {'username': 'carol', 'password': '0xbeefcafebabe'}
bad_login = {'username':'badmin', 'password': 'lol'}

admin_creds = {
    'name': 'Alice Administrator', \
    'address':'Omnipotent', \
    'email':'alice@alice.com', \
    'phonenum':'+313 373 8483', \
    'funds':'31333337'
}
carol_creds = {
    'name': 'Sweet Carolina', \
    'address':'Californ-eye-ay', \
    'email':'carol@candle.lite', \
    'phonenum':'+66 666 6666', \
    'funds':'41424344'
}

DENIEDSTR = b'403 permission denied'
class TestApp:
    # Basic Authentication Tests
    def test_login(self, client):
        res = client.post('/login', data=admin_data, follow_redirects=True)
        assert 'username' in session
        assert b'admin' in res.data

    def test_bad_login(self, client):
        res = client.post('/login', data=bad_login, follow_redirects=True)
        assert 'username' not in session

    def test_no_admin(self, client):
        res = client.get('/admin')
        assert DENIEDSTR in res.data

        res = client.get('/admin?search=admin')
        assert DENIEDSTR in res.data

        res = client.post('/login', data=user_data)
        res = client.get('/admin')
        assert DENIEDSTR in res.data

        res = client.get('/admin?search=admin')
        assert DENIEDSTR in res.data

    # user/me Tests
    def test_me_page(self, client):
        res = client.get('/users/me')
        assert DENIEDSTR in res.data

        res = client.post('/login', data=user_data)
        res = client.get('/users/me')
        assert user_data['username'].encode('utf-8') in res.data

        # Check own creds appear
        assert carol_creds['name'].encode('utf-8') in res.data
        assert carol_creds['address'].encode('utf-8') in res.data
        assert carol_creds['email'].encode('utf-8') in res.data
        assert carol_creds['phonenum'].encode('utf-8') in res.data
        assert carol_creds['funds'].encode('utf-8') in res.data

        assert user_data['username'].encode('utf-8') in res.data

    def test_user_page(self, client):
        res = client.post('/login', data=user_data)
        res = client.get('/users/carol')

        # Check own creds appear
        assert carol_creds['name'].encode('utf-8') in res.data
        assert carol_creds['address'].encode('utf-8') in res.data
        assert carol_creds['email'].encode('utf-8') in res.data
        assert carol_creds['phonenum'].encode('utf-8') in res.data
        assert carol_creds['funds'].encode('utf-8') in res.data

        res = client.get('/users/admin')
        assert DENIEDSTR in res.data

    def test_user_page_admin(self, client):
        res = client.post('/login', data=admin_data)
        res = client.get('/users/admin')

        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data

        res = client.get('/users/carol')

        # Check own creds appear
        assert carol_creds['name'].encode('utf-8') in res.data
        assert carol_creds['address'].encode('utf-8') in res.data
        assert carol_creds['email'].encode('utf-8') in res.data
        assert carol_creds['phonenum'].encode('utf-8') in res.data
        assert carol_creds['funds'].encode('utf-8') in res.data

    # Admin Tests
    def test_admin_page(self, client):
        res = client.get('/admin')
        assert DENIEDSTR in res.data

        res = client.post('/login', data=admin_data)
        res = client.get('/admin')
        assert b'account search' in res.data

        res = client.get('/admin?search=admin')
        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data

        res = client.get('/admin?search=carol')
        assert carol_creds['name'].encode('utf-8') in res.data
        assert carol_creds['address'].encode('utf-8') in res.data
        assert carol_creds['email'].encode('utf-8') in res.data
        assert carol_creds['phonenum'].encode('utf-8') in res.data
        assert carol_creds['funds'].encode('utf-8') in res.data

if __name__ == '__main__':
    unittest.main()
