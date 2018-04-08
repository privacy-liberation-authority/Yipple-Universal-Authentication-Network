# Configure Two Entires in your database like so
# 'type': 'admin'
# 'name': 'Alice Administrator'
# 'address':'Omnipotent'
# 'email':'alice@alice.com'
# 'phonenum':'+313 373 8483'
# 'funds':'31333337'

# 'type': 'user'
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

        res = client.get('/admin?user=admin')
        assert DENIEDSTR in res.data

        res = client.post('/login', data=user_data)
        res = client.get('/admin')
        assert DENIEDSTR in res.data

        res = client.get('/admin?user=admin')
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

        res = client.get('/admin?user=admin')
        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data

        res = client.get('/admin?user=carol')
        assert carol_creds['name'].encode('utf-8') in res.data
        assert carol_creds['address'].encode('utf-8') in res.data
        assert carol_creds['email'].encode('utf-8') in res.data
        assert carol_creds['phonenum'].encode('utf-8') in res.data
        assert carol_creds['funds'].encode('utf-8') in res.data

    def test_credential_edit_success(self, client):
        """Carol can change her own credentials"""
        client.post('/login', data=user_data)

        changed_data = {
            'username': 'carol', # username needs to be a part of the request
            'name': 'Changed Name', \
            'address':'Changed Address', \
            'email':'changed_email@candle.lite', \
            'phonenum':'+99 999 9999', \
            'funds':'99999999'
        }


        res = client.post('/users/me', data=changed_data)
        # Check that carols data has changed
        assert changed_data['name'].encode('utf-8') in res.data
        assert changed_data['address'].encode('utf-8') in res.data
        assert changed_data['email'].encode('utf-8') in res.data
        assert changed_data['phonenum'].encode('utf-8') in res.data
        assert changed_data['funds'].encode('utf-8') in res.data

        # Swap to alice and check her information has not been changed
        client.get('/logout')
        client.post('/login', data=admin_data)

        res = client.get('/users/me', data=changed_data)
        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data

        # Reset the data in the database for sanity's sake
        client.get('/logout')
        client.post('/login', data=user_data)
        reset_data = carol_creds
        reset_data['username'] = 'carol'
        client.post('/users/me', data=reset_data)

    def test_credential_edit_failure(self, client):
        """Carol cannot change Alice's credentials"""
        client.post('/login', data=user_data)

        changed_data = {
            'username': 'admin', # username needs to be a part of the request
            'name': 'Changed Name', \
            'address':'Changed Address', \
            'email':'changed_email@candle.lite', \
            'phonenum':'+99 999 9999', \
            'funds':'99999999'
        }

        # This update should fail, data should not change
        res = client.post('/users/me', data=changed_data)
        assert DENIEDSTR in res.data

        res = client.post('/users/admin', data=changed_data)
        assert DENIEDSTR in res.data

        # Check data has not changed for carol
        res = client.get('/users/me')
        assert carol_creds['name'].encode('utf-8') in res.data
        assert carol_creds['address'].encode('utf-8') in res.data
        assert carol_creds['email'].encode('utf-8') in res.data
        assert carol_creds['phonenum'].encode('utf-8') in res.data
        assert carol_creds['funds'].encode('utf-8') in res.data

        # And check the data has not changed for Alice
        client.get('/logout')
        client.post('/login', data=admin_data)

        res = client.get('/users/me')
        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data


    def test_admin_can_change_others_creds(self, client):
        """Alice can change carols credentials because she is an admin"""
        res = client.post('/login', data=admin_data)

        changed_data = {
            'username': 'carol', # username needs to be a part of the request
            'name': 'Alice changed name', \
            'address':'Alice changed Address', \
            'email':'alice_changed_email@candle.lite', \
            'phonenum':'+88 888 8888', \
            'funds':'88888888'
        }

        res = client.post('/users/carol', data=changed_data)
        assert changed_data['name'].encode('utf-8') in res.data
        assert changed_data['address'].encode('utf-8') in res.data
        assert changed_data['email'].encode('utf-8') in res.data
        assert changed_data['phonenum'].encode('utf-8') in res.data
        assert changed_data['funds'].encode('utf-8') in res.data

        # Check Alice's data hasnt changed
        res = client.get('/users/me')
        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data

        # Reset carols data
        reset_data = carol_creds
        reset_data['username'] = 'carol'
        res = client.post('/users/carol', data=reset_data)

    def test_admin_can_change_others_creds_through_admin_portal(self, client):
        """Alice can change carols credentials through the admin portal because she is an admin"""
        res = client.post('/login', data=admin_data)

        changed_data = {
            'username': 'carol', # username needs to be a part of the request
            'name': 'admin changed name', \
            'address':'admin changed Address', \
            'email':'admin_changed_email@candle.lite', \
            'phonenum':'+88 888 8888', \
            'funds':'88888888'
        }

        res = client.post('/admin', data=changed_data)
        assert changed_data['name'].encode('utf-8') in res.data
        assert changed_data['address'].encode('utf-8') in res.data
        assert changed_data['email'].encode('utf-8') in res.data
        assert changed_data['phonenum'].encode('utf-8') in res.data
        assert changed_data['funds'].encode('utf-8') in res.data

        # Check Alice's data hasnt changed
        res = client.get('/users/me')
        assert admin_creds['name'].encode('utf-8') in res.data
        assert admin_creds['address'].encode('utf-8') in res.data
        assert admin_creds['email'].encode('utf-8') in res.data
        assert admin_creds['phonenum'].encode('utf-8') in res.data
        assert admin_creds['funds'].encode('utf-8') in res.data

        # Reset carols data
        reset_data = carol_creds
        reset_data['username'] = 'carol'
        res = client.post('/admin', data=reset_data)

if __name__ == '__main__':
    unittest.main()
