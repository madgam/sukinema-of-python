from urllib.parse import urlparse
import mysql.connector
import os


class Insert():

    def __init__(self):

        self.title = ''
        self.pref = ''
        self.theater = ''
        self.latitude = 0.0
        self.longitude = 0.0
        self.description = ''
        self.link = ''
        self.time = ''
        self.all_time = ''
        self.review = 0.0
        self.release_date = ''
        self.drop_path = ''
        self.poster_path = ''

    def insert(self, sql_values):

        sql = 'INSERT INTO MOVIES (' + ', '.join([str(k) for k in self.__dict__.keys(
        )]) + ') VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        url = urlparse(os.environ['CLEARDB_DATABASE_URL'])
        conn = mysql.connector.MySQLConnection(
            host=url.hostname,
            port=url.port,
            user=url.username,
            password=url.password,
            database=url.path[1:],
        )
        conn.ping(reconnect=True)
        cur = conn.cursor()

        try:
            cur.executemany(sql, sql_values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
