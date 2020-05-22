
from urllib.parse import urlparse
import mysql.connector
import os


class Registry():

    def addData(self, title, pref, theater, latitude, longitude, description, link, time, allTime, review, releaseDate, dropPath, posterPath):
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

        movie = {
            'title': title,
            'pref': pref,
            'theater': theater,
            'latitude': str(latitude),
            'longitude': str(longitude),
            'description': description,
            'link': link,
            'time': time,
            'all_time': allTime,
            'review': str(review),
            'release_date': releaseDate,
            'drop_path': dropPath,
            'poster_path': posterPath
        }

        sql = 'insert into movies (' + ', '.join([str(k) for k in movie.keys(
        )]) + ') VALUES (' + ', '.join(['\'' + str(v) + '\'' for v in movie.values()]) + ')'

        try:
            cur.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            raise
