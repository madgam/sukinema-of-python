import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from modules import geocoder, registry, common, tmdb


class Scrape():

    def __init__(self):
        self.title = ''
        self.pref = ''
        self.theater = ''
        self.latitude = 0.0
        self.longitude = 0.0
        self.description = ''
        self.link = ''
        self.time = ''
        self.allTime = ''
        self.review = 0.0
        self.releaseDate = ''
        self.dropPath = ''
        self.posterPath = ''

    def getData(self):

        SLASH = '/'
        base_url = 'https://eigakan.org/theaters/pref'
        detail_base_url = 'https://eigakan.org/movies/detail/'
        dt_now = datetime.datetime.now()
        dt_now_y4m2d2 = dt_now.strftime('%Y%m%d')
        reg = registry.Registry()

        for prefID in range(47, 0, -1):
            url = base_url + SLASH + str(prefID) + \
                SLASH + dt_now_y4m2d2

            self.pref = str(prefID)

            page = 1
            while True:
                uri = url + SLASH + str(page)

                res = requests.get(uri)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')

                # ページの終端の場合は処理終了
                isEnd = False
                for tag in soup.find_all(class_='mj03'):
                    isEnd = tag.text.find('存在しません') != -1

                if isEnd:
                    break

                # 映画館・映画情報取得
                theater = soup.select('.theaterlist01 > tr')
                theaterName = ''
                for t in theater:
                    tmp = ''
                    thead = t.find_all(class_='thater_check02')
                    if len(thead) != 0:
                        self.theater = thead[0].text.split('(地図)')[0].strip()
                        theaterName = thead[0].text.split('(地図)')[0].strip()
                        theaterLink = thead[0].find('a')
                        if theaterLink != None:
                            self.link = theaterLink.get('href')

                    if not theaterName or theaterName == '映画館名':
                        continue

                    # 映画館の緯度経度を取得
                    latlong = geocoder.Geocoder.getLatlong(self.theater)
                    self.latitude = latlong['latitude']
                    self.longitude = latlong['longitude']

                    tdata = t.find_all('td')
                    if len(tdata) == 2:
                        self.title = common.Common.cleansing(tdata[0].text)

                        json = tmdb.Tmdb.dataGet(self.title)
                        self.dropPath = ''
                        self.posterPath = ''
                        self.releaseDate = ''
                        self.review = ''
                        if len(json['results']) != 0:
                            json = json['results'][0]

                            if json['backdrop_path'] != None:
                                self.dropPath = json['backdrop_path']

                            if json['poster_path'] != None:
                                self.posterPath = json['poster_path']

                            self.releaseDate = json['release_date']
                            self.review = '{:.1f}'.format(
                                json['vote_average'] / 2)

                        a = tdata[0].find('a')
                        self.description = ''
                        if a != None:
                            detail_base_uri = detail_base_url + a.get('href').split(',')[
                                1].replace('/movies/detail/', '').replace('\'', '')
                            res_detail = requests.get(detail_base_uri)
                            res_detail.raise_for_status()
                            soup_child = BeautifulSoup(
                                res_detail.text, 'html.parser')

                            self.description = common.Common.cleansing(soup_child.find_all(class_='j2')[
                                1].text.split('\n')[0])

                        allTimeAry = [x.split('～')[0].strip() for x in tdata[1].text.split(
                            "/") if not tdata[1].text == '']
                        self.allTime = ','.join(allTimeAry)

                        for oneTime in allTimeAry:
                            self.time = oneTime.split('～')[0]

                            reg.addData(**self.__dict__)
                page += 1
