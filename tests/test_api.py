# -*- coding: UTF-8 -*-
from flask import url_for, json
from base64 import b64encode

from app import db, create_app
from app.models import Role, User

import unittest


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.init_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_header(self, username, password):
        basicstr = b64encode('{}:{}'.format(username, password).encode('utf-8'))
        return {'Authorization': 'Basic {}'.format(basicstr.decode('utf-8')),
                'Accept': 'application/json',
                'Content-Type': 'application/json'}

    def test_no_auth(self):
        response = self.client.get(url_for('api.get_posts'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 403)

    def test_posts(self):
        # add a new user
        r = Role.query.filter_by(name='User').one()
        self.assertIsNotNone(r)
        user = User(email='john@example.com', password='cat', confirmed=True,
                    role=r)
        db.session.add(user)
        db.session.commit()
        # write a post
        response = self.client.post(
                        url_for('api.new_post'),
                        data=json.dumps({'body': 'body of the *blog* post'}),
                        headers=self.get_api_header('john@example.com', 'cat'))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)
        # get this post
        response = self.client.get(url, headers=self.get_api_header('john@example.com', 'cat'))
        self.assertTrue(response.status_code == 200)
        json_res = json.loads(response.get_data(as_text=True))
        self.assertTrue(json_res['url'] == url)
        self.assertTrue(json_res['body'] == 'body of the *blog* post')
        self.assertTrue(json_res['body_html'] == '<p>body of the <em>blog</em> post</p>')
