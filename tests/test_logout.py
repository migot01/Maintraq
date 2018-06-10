import unittest
from app import app
import json
from app.views import user_info

class LogoutUserTestCase(unittest.TestCase):
    """This class represents the api test case"""

    def setUp(self):
        """
        Will be called before every test
        """
        self.client = app.test_client
        self.user = {"username": "patrick", "password": "qwerty123!@#",
                     "first_name": "patrick", "last_name": "Migot"}
        self.logins = {"username": "patrick", "password": "qwerty123!@#"}

        self.register = self.client().post('/api/v1/register', data=json.dumps(self.user),
                                           content_type='application/json')
        self.login = self.client().post('/api/v1/login', data=json.dumps(self.logins),
                                        content_type='application/json')
        self.data = json.loads(self.login.get_data(as_text=True))
        self.token = self.data['auth_token']

    def tearDown(self):
        """ clear data after every test"""
        user_info.users.clear()

    def test_user_can_logout(self):
        """Tests users can logout"""

        logout = self.client().post('/api/v1/logout', data={},
                                    headers={"content_type": "application/json", "access-token": self.token})
        self.assertEqual(logout.status_code, 200)

    def test_user_needs_token_to_logout(self):
        """test that you must be logged for you to logout"""
        res = self.client().post('/api/v1/logout', data={},
                                 headers={"content_type": "application/json"})
        self.assertEqual(res.status_code, 401)
        self.assertIn("Token is missing, login to get token", str(res.data))

    def test_invalid_token(self):
        """Test cannot accept invalid token"""
        logout = self.client().post('/api/v1/logout', data={},
                                    headers={"content_type": "application/json",
                                             "access-token": "wyuweyguy1256"})
        self.assertEqual(logout.status_code, 401)
        self.assertIn("Token is invalid or Expired!", str(logout.data))

    def test_is_logged_out(self):
        """Test user is logged out"""
        self.client().post('/api/v1/logout', data={},
                           headers={"content_type": "application/json",
                                    "access-token": self.token
                                    })
        logout = self.client().post('/api/v1/logout', data={},
                                    headers={"content_type": "application/json",
                                             "access-token": self.token
                                             })
        self.assertEqual(logout.status_code, 401)
        self.assertIn("You are not logged in", str(logout.data))