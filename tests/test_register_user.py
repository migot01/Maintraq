import unittest
from app import app
import json
from app.views import user_info


class CreateUserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client
        self.user = {"username": "patrick", "password": "qwerty123!@#",
                     "first_name": "patrick", "last_name": "migot"}

    def tearDown(self):
        """ clear data after every test"""
        user_info.users.clear()

    def test_user_creation(self):
        """
        Test API can create a user (POST request)
        """
        initial_count = len(user_info.users)
        res = self.client().post('/api/v1/register',
                                data=json.dumps(self.user),
                                headers={"content-type": 'application/json'})
        final_count = len(user_info.users)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(final_count - initial_count, 1)

    def test_cannot_create_duplicate_user(self):
        """
        Tests that duplicate usernames cannot be created
        """
        user1 = self.client().post('/api/v1/register',
                                data=json.dumps(self.user),
                                content_type='application/json')
        user2 = self.client().post('/api/v1/register', 
                                data=json.dumps(self.user),
                                content_type='application/json')
        self.assertIn('Sorry!! Username taken!', str(user2.data))    

   

    def test_details_missing(self):
        """test username and password required"""
        res = self.client().post('/api/v1/register', data=json.dumps({
                                        "username": " ",
                                        "password": " ",
                                        "first_name": "patrick",
                                        "last_name": "migot"
                                    }),
                                 headers={"content-type": 'application/json'})
        self.assertIn('username or password missing' ,str(res.data))

    def test_bad_request(self):
        """test returns bad request if all fields not available"""
        res = self.client().post('/api/v1/register',
                    data=json.dumps({"username": "migot", "last_name": "patrick"}),
                    headers={"content-type": 'application/json'})
        self.assertEqual(res.status_code,400)
        self.assertIn("check you are sending correct information",str(res.data))
    
    def test_password_validation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        res = self.client().post('/api/v1/register',
                    data=json.dumps({
                        "username": "patrick",
                        "password":"123",
                        "first_name": "patrick",
                        "last_name": "migot"
                    }),
                    headers={"content-type": 'application/json'})
        self.assertEqual(res.status_code, 406)
        self.assertIn(
           "Password must be 6-20 Characters",
            str(res.data)
            )

if __name__ == "__main__":
    unittest.main()