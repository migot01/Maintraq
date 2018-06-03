import unittest
from app import app,create_app
import json
from app.views import user_info,request_model

class DeleteBusinessTestCase(unittest.TestCase):
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
            "last_name": "Migot"
        }

        self.logins = {"username": "patrick", "password": "qwerty123!@#"}

        self.request ={
              
              "title": "Repair",
              "location": "Nairobi",
              "body": "Water spill"
              
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
        request_model.requests.clear()

    def test_can_delete_successfully(self):
        """Tests that a request can be Deleted successfully"""
        res = self.client().post('/api/v1/request', data=json.dumps(self.request),
                                 headers={"content-type": "application/json", "access-token": self.token})
        res2 = self.client().delete('/api/v1/request/1',
                                    headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 201)
        self.assertIn("Request Deleted",str(res2.data))

    def test_cannot_delete_empty(self):
        """Tests that cannot delete a request that doesn't exist"""
        res2 = self.client().delete('/api/v1/request/1',
                                    headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(res2.status_code, 401)
        self.assertIn("Request not found",str(res2.data))

