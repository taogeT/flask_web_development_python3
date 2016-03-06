# -*- coding: UTF-8 -*-
from selenium import webdriver
from threading import Thread

from app import create_app, db
from app.models import Role, User, Post

import unittest
import re


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Firefox()
        except:
            pass
        if cls.client:
            # create app
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()
            # create log
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel(logging.ERROR)
            # create database
            db.create_all()
            Role.init_roles()
            User.generate_fake(count=10)
            Post.generate_fake(count=10)
            # add admin
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com', username='john',
                         password='cat', role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()
            # run server in child thread
            Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # close server
            cls.client.get('http://127.0.0.1:5000/shutdown')
            cls.client.close()
            # drop database
            db.session.remove()
            db.drop_all()
            # close context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def test_admin_home_page(self):
        # enter index page
        self.client.get('http://127.0.0.1:5000')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))
        # enter login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)
        # login
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))
        # enter profile page
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>john</h1>' in self.client.page_source)
