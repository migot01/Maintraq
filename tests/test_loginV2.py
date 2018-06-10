import unittest
from app import create_app
import json
from tests.testdb_migrations import migration
from config import conn
import psycopg2
from psycopg2.extras import RealDictCursor
#from app.views2 import user_info

app = create_app("testing")
class LoginuserTestcase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        print(app.url_map)
        migration()
        create_user_statement = """INSERT INTO USERS (first_name,last_name,email,username,password) 
        values('patrick','migot','boss@gmail.com','patrick','qwert@123');"""
        #open a cursor to perform database operations
        self.cur = conn.cursor()
        self.cur.execute(create_user_statement)
        #save it in the database
        conn.commit()
        user_id_statement =("SELECT * FROM users WHERE username='patrick';")
        self.cur.execute(user_id_statement)

        self.client().post('/api/v2/auth/register', data=json.dumps(dict (
                                         first_name = 'patrick',
                                         last_name = 'migot',
                                         email = 'boss@gmail.com',
                                         username = 'patrick',
                                         password = 'qwert@123'
                                    )),
                           headers={"content-type": "application/json"})

    def tearDown(self):
        """ clear data after every test"""
        

    def test_user_can_login(self):
        """Test user can login to get access token"""
        login = self.client().post('/api/v2/auth/login', data=json.dumps(dict (
                                         username = 'patrick',
                                         password = 'qwert@123'
                                    )),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 200)
        self.assertIn("auth_token",str(login.data))

    def test_cannot_login_if_not_registered(self):
        """ Test that only registered users can login"""
          
        login = self.client().post('/api/v2/auth/login', data=json.dumps(dict (
                                         username = 'patrick',
                                         password = 'qwert@123'
                                    )),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 401)
        self.assertIn("Username not found!",str(login.data))

    def test_login_details_required(self):
        """Test that all login fields are required"""
        login = self.client().post('/api/v2/auth/login', 
                        data=json.dumps({"username": "", "password": "23786"}),
                        headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 401)
        self.assertIn("login required!",str(login.data))

    def test_bad_request_with_wrong_filds(self):
        """tests app will only accept required parameters"""
        login = self.client().post('/api/v2/auth/login', data=json.dumps({"password": "23786"}),
                                   headers={"content-type": "application/json"})
        self.assertEqual(login.status_code, 400)
        self.assertIn("check you are sending correct information",str(login.data))

 
if __name__ == "__main__":
    unittest.main()
