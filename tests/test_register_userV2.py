import unittest
from app import app
import json

class CreateUserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.user = {
            
            "email": "john@gmail.com",
            "password": "qwerty123!@#",
            "first_name": "patrick",
            "last_name": "migot"
        }

    def tearDown(self):
        """ clear data after every test"""
        
        

    # def test_user_creation(self):
    #     """
    #     Test API can create a user (POST request)
    #     """
    #     #initial_count = len(User.query.all())
    #     res = self.client().post(
    #         '/api/v2/auth/register',
    #         data=json.dumps(self.user),
    #         headers={"content-type": 'application/json'}
    #     )
    #     #final_count = len(User.query.all())
    #     self.assertEqual(res.status_code, 201)
    #     #self.assertEqual(final_count - initial_count, 1)

    def test_cannot_create_duplicate_user(self):
        """
        Tests that duplicate usernames cannot be created
        """
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        res2 = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        self.assertIn("Email already exists", str(res2.data))

    def test_details_missing(self):
        """test username and password required"""
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
                "first_name": "patrick",
                "last_name": "migot"
            }),
            headers={"content-type": 'application/json'}
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("email or password missing", str(res.data))

    def test_email_cannot_duplicate(self):
        """Test cannot create duplicate emmails"""
        self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        res2 = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps(self.user),
            headers={"content-type": 'application/json'}
        )
        self.assertEqual(res2.status_code, 409)
        self.assertIn("Email already exists", str(res2.data))

    def test_password_validation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        res = self.client().post(
            '/api/v2/auth/register',
            data=json.dumps({
               
                "email": "john@gmail.com",
                "password": "123",
                "first_name": "patrick",
                "last_name": "migot"
            }),
            headers={"content-type": 'application/json'}
        )
        self.assertEqual(res.status_code, 406)
        self.assertIn(
            "Password must be 6-20 Characters",
            str(res.data)
        )


if __name__ == "__main__":
    unittest.main()