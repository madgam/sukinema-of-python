import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from modules import geocoder, common, tmdb, delete, insert
from urllib.parse import urlparse
import mysql.connector
import os
import sys
import time


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
        self.all_time = ''
        self.review = 0.0
        self.release_date = ''
        self.drop_path = ''
        self.poster_path = ''

    def getData(self):

        SLASH = '/'
        base_url = 'https://eigakan.org/theaters/pref'
        detail_base_url = 'https://eigakan.org/movies/detail/'
        dt_now = datetime.datetime.now()
        dt_now_y4m2d2 = dt_now.strftime('%Y%m%d')

        sql_values = []

        for prefID in range(1, 48):
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

                        a = tdata[0].find('a')
                        self.description = ''
                        self.release_date = ''
                        if a != None:
                            detail_base_uri = detail_base_url + a.get('href').split(',')[
                                1].replace('/movies/detail/', '').replace('\'', '')
                            res_detail = requests.get(detail_base_uri)
                            res_detail.raise_for_status()
                            soup_child = BeautifulSoup(
                                res_detail.text, 'html.parser')

                            try:
                                _release_date_split = soup_child.find_all(
                                    class_='j2')[0].text.split('\n')
                                _release_year = _release_date_split[3].replace(
                                    ' ', '').split('年')[0]
                                _release_month_date = _release_date_split[5].replace(
                                    ' ', '').split('より')[0].split('公開')[0]
                                _release_month = _release_month_date.split('月')[
                                    0].zfill(2)
                                _release_date = _release_month.replace(
                                    '日', '').zfill(2)

                                self.release_date = _release_year + '-' + _release_month + '-' + _release_date
                            except Exception as e:
                                self.release_date = ''

                            self.description = common.Common.cleansing(soup_child.find_all(class_='j2')[
                                1].text.split('\n')[0])

                        json = tmdb.Tmdb.dataGet(self.title)
                        self.drop_path = ''
                        self.poster_path = ''
                        self.review = '0.0'
                        if len(json['results']) != 0:

                            sorted_json = sorted(
                                json['results'],
                                key=lambda x: (
                                    x.get(
                                        'popularity', '0.0'),
                                    x.get(
                                        'release_date', '0000-00-00')
                                ),
                                reverse=True
                            )

                            json = sorted_json[0]

                            if json['backdrop_path'] != None:
                                self.drop_path = json['backdrop_path']

                            if json['poster_path'] != None:
                                self.poster_path = json['poster_path']

                            if not self.release_date:
                                self.release_date = json['release_date']

                            self.review = '{:.1f}'.format(
                                json['vote_average'] / 2)
                            if not self.description:
                                self.description = json['overview']

                        allTimeAry = [x.split('～')[0].split('※')[0].strip() for x in tdata[1].text.split(
                            "/") if not tdata[1].text == '']
                        self.all_time = ','.join(allTimeAry)

                        for oneTime in allTimeAry:
                            self.time = oneTime.split('～')[0].split('※')[0]

                            common.Common.createValuesQuery(
                                sql_values, **self.__dict__)
                page += 1

        start = time.time()
        try:
            delete.Delete.delete()
            ins = insert.Insert()
            ins.insert(sql_values)
        except Exception as e:
            raise
        elapsed_time = time.time() - start
        print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
