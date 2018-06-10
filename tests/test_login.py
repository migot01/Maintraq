import unittest
from app import app
from app.views import user_info

import json

class LoginuserTestcase(unittest.TestCase):
    """
    This class implements login user tests
    """
    def setUp(self):
        self.client = app.test_client
        self.user = {"username": "patrick", "password": "qwerty123!@#",
                     "first_name": "patrick", "last_name": "migot"}
        self.logins = {"username": "patrick", "password": "qwerty123!@#"}
        # Create_user
        self.client().post('/api/v1/register', data=json.dumps(self.user),
                           headers={"content-type": "application/json"})

    def tearDown(self):
        """ clear data after every test"""
        user_info.users.clear()

    def test_user_can_login(self):
        """Test user can login to get access token"""
        login = self.client().post('/api/v1/login', data=json.dumps(self.logins),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token",str(login.data))

    def test_cannot_login_if_not_registered(self):
        """ Test that only registered users can login"""
        user_info.users.clear()  # clears users
        login = self.client().post('/api/v1/login', data=json.dumps(self.logins),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 401)
        self.assertIn("Username not found!",str(login.data))

    def test_login_details_required(self):
        """Test that all login fields are required"""
        login = self.client().post('/api/v1/login', 
                        data=json.dumps({"username": "", "password": "23786"}),
                        headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 401)
        self.assertIn("login required!",str(login.data))

    def test_bad_request_with_wrong_filds(self):
        """tests app will only accept required parameters"""
        login = self.client().post('/api/v1/login', data=json.dumps({"password": "23786"}),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 400)
        self.assertIn("check you are sending correct information",str(login.data))

 
if __name__ == "__main__":
    unittest.main()
