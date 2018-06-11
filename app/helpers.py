import psycopg2
from psycopg2.extras import RealDictCursor

GET_USERS = "SELECT * FROM users"
UPDATE_REQUESTS = ""
FETCH_ALL_REQUESTS = "SELECT * FROM requests"
GET_A_SINGLE_REQUEST = "SELECT * FROM requests where id='id'"
GET_USERNAME= "SELECT username FROM users WHERE username=%s"
GET_TOKEN = "SELECT token FROM users"


conn = psycopg2.connect("dbname='maintraq' user='postgres' host='localhost' password='myadmin01?'")

cur = conn.cursor(cursor_factory=RealDictCursor)

def check_email(email):
    user = cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    if not cur.fetchall():
        return True
    return False

def create_user(email, fname, lname, password):
    try:
        cur.execute(u"INSERT INTO USERS (first_name,last_name,email,password,role) values\
                    (%s, %s,%s,%s,0);",(fname, lname, email, password,))
        conn.commit()
    except Exception as ex:
        print(ex)
        return False
   

def get_username(username):
    cur.execute(GET_USERNAME, (username,))
    user = cur.fetchone()
    conn.commit()
    if user:
        return True
    else:
        return  False

def get_user(email):
    cur.execute("SELECT * FROM USERS WHERE email = %s", (email,))
    item = cur.fetchone()
    return item


def create_request(title,location,body,UserID):
    try:
        cur.execute(u"INSERT INTO REQUESTS (title,location,body,status,UserID) values\
                    (%s, %s,%s,'Pending',%s);",(title,location,body,UserID,))
        conn.commit()
        return cur.fetchone()
    except Exception as ex:
        print(ex)
        return False

def get_title(title):
    cur.execute("SELECT * FROM REQUESTS WHERE title = %s", (title,))
    item = cur.fetchone()
    conn.commit()
    return item
def get_requests(UserID):
   cur.execute("SELECT * FROM REQUESTS WHERE UserID=%s",(UserID,))
   requests = cur.fetchall()
   if requests is None:
       return None
   return requests

def get_request(id, user_id):
   cur.execute("SELECT * FROM REQUESTS WHERE id = %s and UserID=%s", (id, user_id,))
   request = cur.fetchone()
   return request

def updated_request(id,title,location,body):
    cur.execute(u"UPDATE requests SET title=%s, location=%s,\
                       body=%s WHERE id=%s;",
                       (title,location,body,id,))
    conn.commit()
    return True

def approve_request(id):
    cur.execute(u"UPDATE requests SET status='Approve' WHERE id = %s;", (id,))
    conn.commit()
    return True

    
def disapprove_request(id):
    cur.execute(u"UPDATE requests SET status='Disapprove' WHERE id = %s;", (id,))
    conn.commit()
    return True

def resolve_request(id):
    cur.execute(u"UPDATE requests SET status='Resolve' WHERE id = %s;", (id,))
    conn.commit()
    return True

def admin_get_all(requests):
    cur.execute("SELECT * FROM REQUESTS ",(requests,))
    requests = cur.fetchall()
    if requests is None:
       return None
    return requests 

def admin_get_request_by_id(id):
    cur.execute("SELECT * FROM REQUESTS WHERE id = %s ", (id,))
    request = cur.fetchone()
    return request
