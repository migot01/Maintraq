import psycopg2

conn = psycopg2.connect("dbname='maintraq' user='postgres' host='localhost' password='myadmin01?'")

cur = conn.cursor()

# create a table

cur.execute("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, first_name varchar,last_name varchar, email varchar, username varchar, password varchar);")

cur.execute("CREATE TABLE IF NOT EXISTS requests(id serial PRIMARY KEY, title varchar, location varchar, body varchar, UserID INT REFERENCES users(ID));")

cur.execute("SELECT * FROM users WHERE username = 'admin'")

admin = cur.fetchone()

if admin is None:
   cur.execute("INSERT INTO users(username, password) VALUES ('admin', 'myadmin01?')")

cur.execute('SELECT * FROM users')

items = cur.fetchone()
print("Migrations done successfully!", items)
conn.commit()