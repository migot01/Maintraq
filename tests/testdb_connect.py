"""
    module to initialize db connections 
    and close them
"""
import os
import psycopg2

class DBConnect():
    def __init__(self):
        """initialize db instance"""

    def connect(self):
        """ create a db conn object """
        try:
            self.conn = psycopg2.connect("dbname='maintraq_test' user='postgres' host='localhost' password='myadmin01?'")
            self.cursor = self.conn.cursor()
            return self.cursor
        except:
            return False

    def close_conn(self):
        """ close cursor and db connection """
        self.cursor.close()
        self.conn.close()