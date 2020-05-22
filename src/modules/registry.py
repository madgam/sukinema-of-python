
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Registry():

    def addData(self, title, pref, theater, latitude, longitude, description, link, time, allTime, review, releaseDate, dropPath, posterPath):
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        # app = firebase_admin.initialize_app(cred)

        if len(firebase_admin._apps) == 0:
            # アプリを初期化する
            default_app = firebase_admin.initialize_app(cred)

        # FIREBASEへの登録
        UB = '_'
        client = firestore.client()
        movie = {
            'title': title,
            'pref': pref,
            'theater': theater,
            'latitude': str(latitude),
            'longitude': str(longitude),
            'description': description,
            'link': link,
            'time': time,
            'allTime': allTime,
            'review': str(review),
            'releaseDate': releaseDate,
            'dropPath': dropPath,
            'posterPath': posterPath
        }

        dt_now = datetime.datetime.now()
        dt_now_y4m2d2 = dt_now.strftime('%Y%m%d')

        doc_ref = client.collection('movies').document(
            dt_now_y4m2d2 + UB + pref + UB + theater + UB + title + UB + time)
        doc_ref.set(movie)
