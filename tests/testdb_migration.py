# create the tables for the application
import psycopg2
from config import conn


def migration():
    cur = conn.cursor()
    

    try:
        # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS requests;")
        cur.execute("DROP TABLE IF EXISTS users;")
        cur.execute("DROP TABLE IF EXISTS users,requests;")


        # create user table
        users = """CREATE TABLE users(id serial PRIMARY KEY, first_name varchar,last_name varchar, email varchar, password varchar,role INT);"""
        # create requests table
        requests = """CREATE TABLE requests(id serial PRIMARY KEY, title varchar, location varchar, body varchar,status varchar, UserID INT REFERENCES users(ID));"""
        cur.execute(users)
        cur.execute(requests)
        conn.commit()

    except Exception as e:
        print('error',e)


migration()