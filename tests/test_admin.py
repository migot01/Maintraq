import unittest
from app import app
import json

class CreateUserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.request = {
             "title": "Repair",
            "location": "Nairobi",
            "body": "dropped laptop",
            "status" : "pending"
        }
        self.user = {
            
            "email": "admin@andela.com",
            "password": "myadmin01?",
            "role": 1
        }


        self.login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.user),
            content_type='application/json'
        )
        self.data = json.loads(self.login.data.decode("utf-8"))
        # get the token to be used by tests
        self.token = self.data['auth_token']

    def test_view_all_requests(self):
        response = self.client().get(
            '/api/v2/requests',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEquals(response.status_code, 200)   

    def test_admin_can_approve_request(self):
        response = self.client().put(
            '/api/v2/requests/1/approve',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEquals(response.status_code, 200)  

    def test_admin_can_disapprove_request(self):
        response = self.client().put(
            '/api/v2/requests/1/disapprove',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEquals(response.status_code, 200)  

    def test_admin_can_resolve_request(self):
        response = self.client().put(
            '/api/v2/requests/1/resolve',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEquals(response.status_code, 200)