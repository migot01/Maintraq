import unittest
import json
from app import app
from app.views import request_model
import os



class RequeststestCase(unittest.TestCase):

    def setUp(self):
        """
        will be called before every test
        """
        self.client = app.test_client
        self.user = {"username": "patrick", "password": "qwerty123!@#",
                     "first_name": "patrick", "last_name": "migot"}

        self.logins = {"username": "patrick", "password": "qwerty123!@#"}

        self.request = {
              "title": "repairs",
              "location": "nairobi",
              "body": "spilled water on my laptop"
              }
        self.empty_request = {"title": "", "location": "",
                              "body": ""}

       
        self.client().post('/api/v1/register', data=json.dumps(self.user),
                           content_type='application/json')

        self.login = self.client().post('/api/v1/login', data=json.dumps(self.logins),
                                        content_type='application/json')

        self.data = json.loads(self.login.data.decode('UTF-8'))
        # get the token to be used by tests
        self.token = self.data["auth_token"]

     
    def tearDown(self):
        """ clear data after every test"""
        request_model.requests.clear()

    

    def test_request_can_create_successfully(self):
        """Tests that a request can be created successfully"""
        initial_count = len(request_model.requests)
        res = self.client().post('/api/v1/request', data=json.dumps(self.request),
                                 headers={"content-type": "application/json", "access-token": self.token})
        final_count = len(request_model.requests)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)
        self.assertIn("Request created",str(res.data))
    
    def test_cannot_create_duplicate(self):
        """Tests that no two requests can exist with similar title"""
        title1 = self.client().post('/api/v1/request',
                    data=json.dumps(self.request),
                    headers={
                        "content-type": "application/json",
                        "access-token": self.token
                    })
        title2 = self.client().post('/api/v1/request', data=json.dumps(self.request),
                                  headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(title2.status_code, 401)
        
        self.assertIn("Sorry!! Name taken!",str(title2.data))

    def test_cannot_create_with_name(self):
        """Tests that request title, location and body must be provided to create an new request"""
        res = self.client().post('/api/v1/request', data=json.dumps(self.empty_request),
                                 headers={"content-type": "application/json", "access-token": self.token})
        
        self.assertIn("Name cannot be empty!",str(res.data))

    
    