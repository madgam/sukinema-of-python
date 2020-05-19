import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# SLASH = '/'
# base_url = 'https://eigakan.org/theaters/pref'
# dt_now = datetime.datetime.now()
# dt_now_y4m2d2 = dt_now.strftime('%Y%m%d')
# page = 1

# for prefID in range(46, 0, -1):

#     uri = base_url + SLASH + str(prefID) + \
#         SLASH + dt_now_y4m2d2 + str(page)
#     res = requests.get(uri)
#     res.raise_for_status()
#     soup = BeautifulSoup(res.text, "html.parser")

#     # print(soup.title.string.strip())
#     # print(soup.findAll('a'))

#     tags = soup.findAll('a')
#     for tag in tags:
#         print(tag.get('href'))

#     break

cred = credentials.Certificate("path/to/serviceAccountKey.json")

app = firebase_admin.initialize_app(cred)

client = firestore.client()
# docs = client.collection('movies').stream()

# for doc in docs:
#     # print('{} => {}'.format(doc.id, doc.to_dict()))
#     print(doc.to_dict())

movie = {}
movie['title'] = 'test'
movie['pref'] = '14'
movie['theater'] = 'testTheater'
movie['latitude'] = '1.22222'
movie['longitude'] = '2,11111'
movie['description'] = 'testtesttesttest'
movie['link'] = 'http://test.com'
movie['time'] = '12:50'
movie['allTime'] = '12:50,15:00,17:30'
movie['review'] = '4.2'
movie['releaseDate'] = '2018-12-20'
movie['dropPath'] = 'xxxxxx.png'
movie['posterID'] = 'xxxxxx'
doc_ref = client.collection('movies').document()
doc_ref.set(movie)
