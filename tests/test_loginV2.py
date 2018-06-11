import unittest
from app import app
from app.views2 import User


import json

class LoginuserTestcase(unittest.TestCase):
    """
    This class implements login user tests
    """
    def setUp(self):
        self.client = app.test_client
        
        self.user = {
            
            "email": "migot@gmail.com",
            "password": "qwerty123!@#",
            "first_name": "patrick",
            "last_name": "Migot"
        }
        self.logins = {
            "email": "migot@gmail.com",
            "password": "qwerty123!@#"
        }

    def tearDown(self):
        """ clear data after every test"""
        

    def test_user_can_login(self):
        """Test user can login to get access token"""
        # Create_user
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": "application/json"}
        )
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps(self.logins),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token", str(login.data))

    def test_cannot_login_if_not_registered(self):
        """ Test that only registered users can login"""
        
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps({
            "email": "job@gmail.com",
            "password": "qwerty123!@#"
        }),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 404)
        self.assertIn("User does not exist", str(login.data))

    def test_login_details_required(self):
        """Test that all login fields are required"""
        login = self.client().post(
            '/api/v2/auth/login',
            data=json.dumps({
                "email": "",
                "password": ""
            }),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(login.status_code, 401)
        self.assertIn("login required!", str(login.data))


if __name__ == "__main__":
    unittest.main()