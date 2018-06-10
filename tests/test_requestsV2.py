import unittest
from app import app
import json
# from tests.testdb_migration import migration
# from config import conn
import psycopg2
from psycopg2.extras import RealDictCursor
#from app.views2 import user_info

#app = create_app("testing")
class RequeststestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.user = {
            
            "email": "moses@gmail.com",
            "password": "qwerty123!@#",
            "first_name": "patrick",
            "last_name": "migot"
        }

        self.logins = {
            "email": "moses@gmail.com",
            "password": "qwerty123!@#"
        }

        self.request = {
             "title": "Repair",
            "location": "Nairobi",
            "body": "dropped laptop"
        }
        
        self.update_request = {
            "title": "",
              "location": "",
              "body": ""
        }

        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            content_type='application/json'
        )

        self.login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.logins),
            content_type='application/json'
        )
        self.data = json.loads(self.login.data.decode("utf-8"))
        # get the token to be used by tests
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
                    
   
    def test_api_for_user_create_request(self):
        response = self.client().post(
            '/api/v2/Auth/request',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        
        self.assertEquals(response.status_code, 201)

    def test_api_for_user_read_all_request(self):
        #test endpoint for user to view requests
        response = self.client().get(
            '/api/v2/users/requests',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEquals(response.status_code, 200)

    def test_api_to_view_a_request(self):
        #test api to view request
        response = self.client().get(
            '/api/v2/users/requests/1',
            data=json.dumps(self.request),
            headers={
                "content-type": "application/json",
                "access-token": self.token
            }
        )
        self.assertEquals(response.status_code, 200)

    def test_api_to_update_a_request(self):
        #test api to update a request
        res = self.client().post('/api/v2/Auth/request', data=json.dumps(self.request),
                                 headers={"content-type": "application/json",
                                          "access-token": self.token})
        res2 = self.client().put('/api/v2/users/requests/1', data=json.dumps(self.update_request),
                                 headers={"content-type": "application/json",
                                          "access-token": self.token})
        
        self.assertEquals(res2.status_code, 200)
        
        

    