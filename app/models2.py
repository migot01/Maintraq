import psycopg2

GET_USERS = "SELECT * FROM users"
UPDATE_REQUESTS = ""
FETCH_ALL_REQUESTS = "SELECT * FROM requests"
GET_A_SINGLE_REQUEST = "SELECT * FROM requests where id='id'"
GET_USERNAME= "SELECT username FROM users"


conn = psycopg2.connect("dbname='maintraq' user='postgres' host='localhost' password='myadmin01?'")

cur = conn.cursor()

def get_users(username):
    #cur.execute(GET_USERS)
   cur.execute(GET_USERS)
   items = cur.fetchall()
   conn.commit()
   return items


def create_user(user):
   cur.execute("INSERT INTO USERS (first_name,last_name,email,username,password) values(%s,%s,%s,%s,%s)",(
       user['first_name'] ,
       user['last_name'],
       user['email'],
       user['username'],
       user['password']))
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
    print(item)
    return {
        "id": item[0],
        "first_name": item[1],
        "last_name": item[2],
        "email": item[3],
        "username": item[4],
        "password": item[5]
    }

   
   