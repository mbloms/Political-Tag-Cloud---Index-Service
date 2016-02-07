# Using Twithon, install with sudo pip3 install twython

import psycopg2

class Database:
    def __init__(self):
        try:

            self.conn = psycopg2.connect(database="lcd", user="postgres", password="asd", host="localhost", port="5432")

            self.cur = self.conn.cursor()
        except:
            print ("I am unable to connect to the database")

    def cursor(self):
        return self.cur

    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.close()

