import unittest, json
from main import Flask,db,app
from flask_testing import TestCase

class TestUserRegister(TestCase):
    def create_app(self):
        app.config.from_object('configs.DbConfig.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_userRegistration(self):
        # given
        user = json.dumps({
            'full_name':'Mark Gee',
            'email':'mark@gmail.com',
            'password':'123'
        })
        response = self.client.post('/api/v1/register', headers={"Content-Type": "application/json"}, data=user)
        res_data = json.loads(response.data)
        # then
        self.assertEqual(response.status_code,201)
        self.assertTrue(res_data['access_token'])

        
