import unittest
from app import app
import json


class CreateUserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.client=self.app.test_client
        self.user={"username":"patrick", "password":"abc.123!",
        "first_name":"patrick","last_name":"migot"
        }

    def test_user_creation(self):
        """
        Test that the API can create a user
        """
        res=self.client().post('/api/v1/register',data=json.dumps(self.user),
                                                  headers={"content-type":"application/json"})

        self.assertEqual(res.status_code,201)

    def test_cannot_create_duplicate_user(self):
        """
        Tests duplicate names cannot be created
        """
        res=self.client().post('/api/v1/register',data=json.dumps(self.user),
                                                  headers={"content-type":"application/json"})
        res2=self.client().post('/api/v1/register',data=json.dumps(self.user),
                                                  headers={"content-type":"application/json"})
        assert b'{\n "message":"username already taken"\n}n' in res.data

    def test_password validation(self):
        """
        test that password must be more than 6 characters
        """
        res=self.client().post('/api/v1/register', 
                        data=json.dumps({
                            "username":"patrick",
                            "password":"abc",
                            "first_name":"patrick",
                            "last_name":"migot"
                        }),
                        headers={"content-type":"application/json"}
                        )
        self.assertEqual(res.status_code, 406)
        self.asserIn("password must be more than 6 characters", str(res.data))                                  