import unittest
from app import create_app
import json
from tests.testdb_migrations import migration
from config import conn
import psycopg2
from psycopg2.extras import RealDictCursor
#from app.views2 import user_info

app = create_app("testing")
class CreateUserTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        print(app.url_map)
        migration()
        create_user_statement = """INSERT INTO USERS (first_name,last_name,email,password) 
        values('patrick','migot','boss@gmail.com','qwert@123');"""
        #open a cursor to perform database operations
        self.cur = conn.cursor()
        self.cur.execute(create_user_statement)
        #save it in the database
        conn.commit()
        user_id_statement =("SELECT * FROM users WHERE email='boss@gmail.com';")
        self.cur.execute(user_id_statement)
          
   

    def tearDown(self):
        """ clear the data and variables set during testing """
      


    def test_cannot_create_duplicate_user(self):
        """
        Tests that duplicate usernames cannot be created
        """
        user1 = self.client.post('/api/v2/auth/register',
                                data=json.dumps(dict (
                                         first_name = 'patrick',
                                         last_name = 'migot',
                                         email = 'boss@gmail.com',
                                         password = 'qwert@123'
                                    )), content_type = 'application/json')
        user2 = self.client.post('/api/v2/auth/register', 
                                data=json.dumps(dict (
                                         first_name = 'patrick',
                                         last_name = 'migot',
                                         email = 'boss@gmail.com',
                                         password = 'qwert@123'
                                    )),
                                content_type='application/json')
        self.assertIn('Sorry!! Username taken!', str(user2.data))    

   

    def test_details_missing(self):
        """test username and password required"""
        res = self.client.post('/api/v2/auth/register', data=json.dumps(dict (
                                         first_name = 'patrick',
                                         last_name = 'migot',
                                         email = 'boss@gmail.com',
                                         password = ''
                                    )),
                                 headers={"content-type": 'application/json'})
        self.assertIn('email or password missing' ,str(res.data))

    def test_bad_request(self):
        """test returns bad request if all fields not available"""
        res = self.client.post('/api/v2/auth/register',
                    data=json.dumps(dict (                                        
                                         last_name = 'migot',
                                         first_name = 'patrick'
                                    )),
                    headers={"content-type": 'application/json'})
        print(res)
        self.assertEqual(res.status_code, 400)
        self.assertIn("check you are sending correct information",str(res.data))
    
    def test_password_validation(self):
        """Test password must be 6-20 characters, alphanumeric"""
        res = self.client.post('/api/v2/auth/register',
                    data=json.dumps({
                        "password":"123",
                        "first_name": "patrick",
                        "last_name": "migot",
                        "email" : "boss@gmail.com"
                    }),
                    content_type='application/json')
        self.assertEqual(res.status_code, 406)
        self.assertIn(
           "Password must be 6-20 Characters",
            str(res.data)
            )

if __name__ == "__main__":
    unittest.main()