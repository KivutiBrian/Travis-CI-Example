from main import app,db
import unittest
import json
from models.UserModel import UserModel
from configs.DbConfig import TestingConfig
from datetime import datetime
from flask_testing import TestCase
from flask import Flask
from werkzeug.security import generate_password_hash

class TestLogin(TestCase):
    
    def create_app(self):
        app.config.from_object('configs.DbConfig.TestingConfig')
        return app


    def setUp(self):
        # app.config.from_object('configs.DbConfig.TestingConfig')
        db.create_all()
        user = UserModel(full_name="Test User",email="test@gmail.com", password=generate_password_hash("123"))
        user.create_record()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_successful_login(self):
        # given
        user_payload = json.dumps({"email":"test@gmail.com","password":"123"})
        response = self.client.post('/api/v1/login', headers={"Content-Type": "application/json"}, data=user_payload)
        # then
        self.assertEqual(response.status_code,200) 
        self.assertEqual(type(response.json['access_token']),str)
        self.assertEqual(response.is_json, True) 


    def test_unsuccessful_login(self):
        # given
        user_payload = json.dumps({"email":"test@gmail.com","password":"888"})
        response = self.client.post('/api/v1/login', headers={"Content-Type": "application/json"}, data=user_payload)

        # Then
        self.assertEqual(response.status_code,401)


    def test_invalid_payload(self):
        # given an issue in email key in your payload
        user_payload = json.dumps({"ema":"test@gmail.com","password":"123"})
        response = self.client.post('/api/v1/login', headers={"Content-Type": "application/json"}, data=user_payload)

        # Then
        self.assertEqual(response.status_code,400)

        # given an issue in password key in your payload
        user_payload = json.dumps({"email":"test@gmail.com","passw":"123"})
        response = self.client.post('/api/v1/login', headers={"Content-Type": "application/json"}, data=user_payload)

        # Then
        self.assertEqual(response.status_code,400)


# if __name__ == '__main__':
#     unittest.main()