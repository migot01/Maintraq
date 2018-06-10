import psycopg2

conn = psycopg2.connect("dbname='maintraq' user='postgres' host='localhost' password='myadmin01?'")

cur = conn.cursor()

# create a table
cur.execute("DROP TABLE IF EXISTS requests;")
cur.execute("DROP TABLE IF EXISTS users;")


cur.execute("CREATE TABLE IF NOT EXISTS users\
        (id serial PRIMARY KEY, first_name varchar,\
        last_name varchar, email varchar, password varchar,\
        role INT);")

cur.execute("CREATE TABLE IF NOT EXISTS requests\
(id serial PRIMARY KEY, title varchar, \
location varchar, body varchar,status varchar, UserID INT REFERENCES users(ID));")

cur.execute("SELECT * FROM users WHERE email = 'admin@andela.com'")

admin = cur.fetchone()

if admin is None:
   cur.execute("INSERT INTO users(email, password, role) VALUES ('admin@andela.com', 'myadmin01?', 1)")

cur.execute('SELECT * FROM users')

items = cur.fetchone()
print("Migrations done successfully!", items)
conn.commit()