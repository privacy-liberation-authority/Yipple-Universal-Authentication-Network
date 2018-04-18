#!/usr/bin/env python3
import unittest
import urllib3
import time

from flask import abort, url_for
from flask_testing import TestCase, LiveServerTestCase
from selenium import webdriver

from komradebank import create_app
from komradebank.models import db, User, Acct, Xact

loadWait = 0.1

adminName = 'admin'
adminPass = 'alice'
userName = 'carol'
userPass = '0xbeefcafebabe'


class TestUnitBase(TestCase):

    def create_app(self):
        app = create_app()
        return app

    # called BEFORE every test
    def setUp(self):
        db.drop()
        db.create()

    # called AFTER every test
    def tearDown(self):
        pass


class TestModels(TestUnitBase):

    def test_user_model(self):

        # new users can be added
        count = len(User.by_filter(''))
        user_id = User.new('username', 'password')
        self.assertEqual(user_id, count+1)

    def test_acct_model(self):

        # new accounts can be added
        count = len(Acct.by_filter(''))
        Acct.new(0)
        new_count = len(Acct.by_filter(''))
        self.assertEqual(new_count, count+1)

    def test_xact_model(self):

        # new xacts can be added
        acct_id = Acct.by_user_id(1)[0].id
        count = len(Xact.by_filter(''))
        xact_id = Xact.new(acct_id, 'test transaction', 1.00)
        self.assertEqual(xact_id, count+1)

    def test_register_user(self):

        # create new user
        user_id = User.new('username', 'password')

        # validate user receives one account
        accts = Acct.by_user_id(user_id)
        self.assertEqual(len(accts), 1)

        # validate user's account starts with 2 transactions
        # 1. Starting Balance   0.00
        # 2. New Account Offer  1337.00
        xacts = Xact.by_acct_id(accts[0].id)
        self.assertEqual(len(xacts), 2)


class TestViews(TestUnitBase):

    def test_index_view(self):

        # / is accessible by unauthenticated users
        resp = self.client.get(url_for('.index'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view(self):

        # /login is accessible by unauthenticated users
        resp = self.client.get(url_for('.login'))
        self.assertEqual(resp.status_code, 200)

    def test_logout_view(self):

        # /logout redirects to /login for unauthenticated users
        target_url = url_for('.logout')
        redirect_url = url_for('.login', next=target_url)
        resp = self.client.get(target_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, redirect_url)

    def test_admin_view(self):

        # /admin redirects to /login for unauthenticated users
        target_url = url_for('.admin')
        redirect_url = url_for('.login', next=target_url)
        resp = self.client.get(target_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, redirect_url)


class TestIntegrationBase(LiveServerTestCase):

    def create_app(self):
        app = create_app()
        return app

    # called BEFORE every test
    def setUp(self):
        self.http = urllib3.PoolManager()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1280,720');
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(self.get_server_url())
        db.drop()
        db.create()

    # called AFTER every test
    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):

        # Click 'Login'
        self.driver.find_element_by_id("btnLogin").click()
        time.sleep(loadWait)

        # Assert that browser redirects to login page
        assert url_for('.login') in self.driver.current_url

        # Fill in login form
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(loadWait)

        # Assert that browser redirects to index page
        assert url_for('.index') in self.driver.current_url

        # Assert success message is shown
        msg = self.driver.find_element_by_class_name("alert").text
        assert "Logged in successfully." in msg

    def logout(self):

        # Click 'Logout'
        self.driver.find_element_by_id("btnLogout").click()
        time.sleep(loadWait)

        # Assert we're redirected to unauthenticated index.
        assert 'BLOCKCHAIN' in self.driver.find_element_by_class_name("jumbotron").text

    def edit_details(self, user, password=''):

        # Assert that browser redirects to edit page
        assert url_for('.edit', username=user.name) in self.driver.current_url

        # Fill in edit form
        if user.is_admin():
            self.driver.find_element_by_id("role").clear()
            self.driver.find_element_by_id("role").send_keys(user.role)
        self.driver.find_element_by_id("fullname").clear()
        self.driver.find_element_by_id("fullname").send_keys(user.fullname)
        self.driver.find_element_by_id("phone").clear()
        self.driver.find_element_by_id("phone").send_keys(user.phone)
        self.driver.find_element_by_id("email").clear()
        self.driver.find_element_by_id("email").send_keys(user.email)
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(loadWait)

        # Assert that browser redirects to index (or admin) page
        assert url_for('.index') in self.driver.current_url or url_for('.admin') in self.driver.current_url

        # Assert success message is shown
        msg = self.driver.find_element_by_class_name("alert").text
        assert "Successfully updated details." in msg

    def transfer(self, user_id, memo, amount):

        # Assert that browser redirects to edit page
        assert url_for('.xfer') in self.driver.current_url

        # Transfer details
        acct_id = Acct.by_user_id(user_id)[0].id

        # Fill in transfer form
        self.driver.find_element_by_id("dst").clear()
        self.driver.find_element_by_id("dst").send_keys(acct_id)
        self.driver.find_element_by_id("memo").clear()
        self.driver.find_element_by_id("memo").send_keys(memo)
        self.driver.find_element_by_id("amount").clear()
        self.driver.find_element_by_id("amount").send_keys(amount)
        self.driver.find_element_by_id("submit").click()
        time.sleep(loadWait)

        # Assert that browser redirects to index page
        assert url_for('.index') in self.driver.current_url

        # Assert success message is shown
        msg = self.driver.find_element_by_class_name("alert").text
        assert "Funds transferred successfully." in msg

        return acct_id


class TestAuthentication(TestIntegrationBase):

    def test_login_logout(self):
        self.login(adminName, adminPass)

        # Validate by checking user specific data is present
        assert self.driver.find_element_by_id("user_fullname").text == "Alice Administrator"

        self.logout()


class TestRegistration(TestIntegrationBase):

    def test_registration_success(self):

        # Click 'Register Now'
        self.driver.find_element_by_id("btnRegister").click()
        time.sleep(loadWait)

        # Assert that browser redirects to register page
        assert url_for('.register') in self.driver.current_url

        # New user data
        username = 'testUser'
        password = 'testPass'

        # Fill in registration form
        count = len(User.by_filter(''))
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(loadWait)

        # Assert that browser redirects to login page
        assert url_for('.login') in self.driver.current_url

        # Assert success message is shown
        msg = self.driver.find_element_by_class_name("alert").text
        assert "Registration successful!" in msg

        # Assert that there are now 3 employees in the database
        self.assertEqual(len(User.by_filter('')), count+1)


class TestEditDetails(TestIntegrationBase):

    def test_edit_details_success(self):
        self.login(userName, userPass)

        # Click 'Edit Details'
        self.driver.find_element_by_id("btnEditDetails").click()
        time.sleep(loadWait)

        # Updated details
        newEmail = 'new@email.com'
        newPassword = 'taylorswift'

        # Submit edit form
        u = User.by_name(userName)
        u.email = newEmail
        self.edit_details(u, newPassword)

        # Validate updated email
        assert self.driver.find_element_by_id("user_email").text == newEmail

        # Validate new password
        self.logout()
        self.login(userName, newPassword)


class TestTransfer(TestIntegrationBase):

    def test_transfer_success(self):
        self.login(userName, userPass)

        # Click 'Transfer'
        self.driver.find_element_by_id("btnTransfer").click()
        time.sleep(loadWait)

        # Assert that browser redirects to edit page
        assert url_for('.xfer') in self.driver.current_url

        # Transfer details
        xferMemo = 'wubba lubba dub dub!'
        xferAmount = '9447.00'

        # Perform the transfer
        acct_id = self.transfer(2, xferMemo, xferAmount)

        # Validate transaction appears on index page.
        assert xferMemo in self.driver.find_element_by_id("xfer-table").text

        # Validate transaction appears in other user's account.
        xacts = Xact.by_acct_id(acct_id)
        assert xacts[0].memo == xferMemo and xacts[0].amount == float(xferAmount)


class TestAdmin(TestIntegrationBase):

    def test_admin_edit_other_user(self):
        self.login(adminName, adminPass)

        # Click 'Admin'
        self.driver.find_element_by_id("btnAdmin").click()
        time.sleep(loadWait)

        # Click on user row
        uid = 4
        self.driver.find_element_by_id("user_" + str(uid)).click()
        time.sleep(loadWait)

        # Perform edit
        u = User.by_id(uid)
        u.fullname = 'Badmin'
        self.edit_details(u)

        # Validate change by checking user row
        assert 'Badmin' in self.driver.find_element_by_id("user_" +str(uid)).text


if __name__ == '__main__':
    unittest.main(warnings='ignore')
    unittest.main()

