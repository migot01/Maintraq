import psycopg2
from psycopg2.extras import RealDictCursor

GET_USERS = "SELECT * FROM users"
UPDATE_REQUESTS = ""
FETCH_ALL_REQUESTS = "SELECT * FROM requests"
GET_A_SINGLE_REQUEST = "SELECT * FROM requests where id='id'"
GET_USERNAME= "SELECT username FROM users"
GET_TOKEN = "SELECT token FROM users"


conn = psycopg2.connect("dbname='maintraq' user='postgres' host='localhost' password='myadmin01?'")

cur = conn.cursor(cursor_factory=RealDictCursor)


def create_user(user):
   cur.execute("INSERT INTO USERS (first_name,last_name,email,username,password) values(%(first_name)s, %(last_name)s,%(email)s,%(username)s,%(password)s)",(user))
   conn.commit()

def get_username(username):
    cur.execute(GET_USERNAME)
    items = cur.fetchall()
    conn.commit()
    return  items

def get_user(username):
    cur.execute("SELECT * FROM USERS WHERE username = %s", (username,))
    item = cur.fetchone()
    conn.commit()
    return item


def create_request(requests):
    cur.execute("INSERT INTO REQUESTS (title,location,body,UserID) values(%s,%s,%s,%s)",(
       requests['title'] ,
       requests['location'],
       requests['body'],
       requests['UserID']))

def get_title(title):
    cur.execute("SELECT * FROM REQUESTS WHERE title = %s", (title,))
    item = cur.fetchone()
    conn.commit()
    return item
        
    



   
   