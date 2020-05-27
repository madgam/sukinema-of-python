from urllib.parse import urlparse
import mysql.connector
import os


class Delete():

    @classmethod
    def delete(cls):

        sql = 'DELETE FROM MOVIES'

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
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
