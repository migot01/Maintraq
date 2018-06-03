import unittest
import json
from app import app,create_app
from app.views import request_model
import os

class CreateUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.client = app.test_client
        self.user = {
            "username": "patrick",
            "password": "qwerty123!@#",
            "first_name": "patrick",
            "last_name": "migot"
        }

        self.logins = {"username": "patrick", "password": "qwerty123!@#"}

        self.request = {
              "title": "repairs",
              "location": "nairobi",
              "body": "spilled water on my laptop"
              }
        self.update_request = {
            "title": "",
              "location": "",
              "body": ""
        }
        self.client().post(
            '/api/v1/register',
            data=json.dumps(self.user),
            content_type='application/json'
        )

        self.login = self.client().post(
            '/api/v1/login',
            data=json.dumps(self.logins),
            content_type='application/json'
        )
        self.data = json.loads(self.login.get_data(as_text=True))
        # get the token to be used by tests
        self.token = self.data['auth_token']

    def tearDown(self): 
        """ clear data after every test"""

    def test_request_can_updated_successfully(self):
        """Tests that a request can be updated successfully"""
        request_model.requests.clear()
        res = self.client().post('/api/v1/request', data=json.dumps(self.request),
                                 headers={"content-type": "application/json",
                                          "access-token": self.token})
        res2 = self.client().put('/api/v1/request/1', data=json.dumps(self.update_request),
                                 headers={"content-type": "application/json",
                                          "access-token": self.token})
        self.assertEqual(res2.status_code, 202)
        self.assertIn("request updated!",str(res2.data))


    def test_can_get_request(self):
        """test can get all requests"""
        request_model.requests.clear()
        self.client().post('/api/v1/request', data=json.dumps(self.request),
                           headers={"content-type": "application/json",
                                    "access-token": self.token})
        res = self.client().get('/api/v1/request',
                                headers={"access-token": self.token})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(request_model.requests), 1)

  
        
        
 