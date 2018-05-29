import unittest

import json

class LoginuserTestcase(unittest.TestCase):
    """
    This class implements login user tests
    """
    def setUp(self):
        self.app=create_app(config_name="testing")
        self.client=self.app.test_client
        self.user={"username":"patrick", "password":"abc.123!",
                   "first_name":"patrick","last_name": "ochieng"}
        self.logins={"username":"patrick", "password":"abc.123!"}


    def test_user_can_login(self):
        login=self.client().post('/api/v1/login',data=json.dumps(self.login),
                              headers={"content-type":"applocation/json"})
        self.assertEqual(login.status_code,200)

    def test_cannot_login_if_not_registered(self):
        login=self.client().post('/api/v1/login',data=json.dumps(self.login),
                              headers={"content-type":"applocation/json"})
        self.assertEqual(login.status_code,401)
        self.assertIn ("username not found!",login.data)

    def test_login_details_required(self):
        login=self.client().post('/api/v1/login',data=json.dumps(self.login),
                              headers={"content-type":"applocation/json"})
        self.assertEqual(login.status_code,400)
        self.assertIn("Login required",login.data)
