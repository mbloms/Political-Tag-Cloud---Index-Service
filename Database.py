import psycopg2
import DatabaseConfig as DC

class Database:
    def __init__(self):
        conf = DC.DatabaseConfig("config/dbconfig.json","testdb")
        try:
            self.conn = psycopg2.connect(database=conf.database, user=conf.user, password=conf.password, host=conf.host, port=conf.port)

            self.cursor = self.conn.cursor()
        except:
            print ("I am unable to connect to the database")

    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.close()

