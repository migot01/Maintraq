import unittest
from app import create_app
import json
from tests.testdb_migrations import migration
from config import conn
import psycopg2
from psycopg2.extras import RealDictCursor
#from app.views2 import user_info

app = create_app("testing")
class RequeststestCase(unittest.TestCase):
    
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
        create_Request = """INSERT INTO REQUESTS (title,location,body) 
        values('Repair','Nairobi','Need a new laptop');"""
        #open a cursor to perform database operations
        self.cur = conn.cursor()
        self.cur.execute(create_Request)
        #save it in the database
        conn.commit()
        request_id_statement =("SELECT * FROM requests WHERE title='repair';")
        self.cur.execute(request_id_statement)
        

        self.client().post('/api/v2/auth/register', data=json.dumps(dict (
                                         first_name, = 'patrick',
                                         last_name = 'migot',
                                         email = 'boss@gmail.com',
                                         username = 'patrick',
                                         password = 'qwert@123'
                                    )),
                           content_type='application/json')

        self.login = self.client().post('/api/v2/auth/login', data=json.dumps({"username": "patrick", "password": "qwert@123"}),
                                        content_type='application/json')

        self.data = json.loads(self.login.data.decode('UTF-8'))
        self.token = self.data["auth_token"]

    def tearDown(self):
        """ clear data after every test"""
        

    

    def test_request_can_create_successfully(self):
        """Tests that a request can be created successfully"""
        #initial_count = len(request_model.requests)
        res = self.client().post('/api/v2/Auth/request', data=json.dumps({
              "title": "repairs",
              "location": "nairobi",
              "body": "spilled water on my laptop"
              }),
                                 headers={"content-type": "application/json", "access-token": self.token})
        #final_count = len(request_model.requests)
        self.assertEqual(res.status_code, 201)
        #self.assertEqual(final_count - initial_count, 1)
        self.assertIn("Request created",str(res.data))
    
    def test_cannot_create_duplicate(self):
        """Tests that no two requests can exist with similar title"""
        title1 = self.client().post('/api/v2/Auth/request',
                    data=json.dumps({
              "title": "repairs",
              "location": "nairobi",
              "body": "spilled water on my laptop"
              }),
                    headers={
                        "content-type": "application/json",
                        "access-token": self.token
                    })
        title2 = self.client().post('/api/v2/Auth/request', data=json.dumps({
              "title": "repairs",
              "location": "nairobi",
              "body": "spilled water on my laptop"
              }),
                                  headers={"content-type": "application/json", "access-token": self.token})
        self.assertEqual(title2.status_code, 401)
        
        self.assertIn("Sorry!! Name taken!",str(title2.data))

    def test_cannot_create_with_name(self):
        """Tests that request title, location and body must be provided to create an new request"""
        res = self.client().post('/api/v2/Auth/request', data=json.dumps( {"title": "", "location": "",
                              "body": ""}),
                                 headers={"content-type": "application/json", "access-token": self.token})
        
        self.assertIn("Name cannot be empty!",str(res.data))
          