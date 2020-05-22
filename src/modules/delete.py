from urllib.parse import urlparse
import mysql.connector
import os


class Delete():

    @classmethod
    def delete(cls):

        url = urlparse(os.environ['CLEARDB_DATABASE_URL'])
        conn = mysql.connector.connect(
            host=url.hostname,
            port=url.port,
            user=url.username,
            password=url.password,
            database=url.path[1:],
        )
        conn.ping(reconnect=True)
        cur = conn.cursor()

        sql = 'DELETE FROM MOVIES'

        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
