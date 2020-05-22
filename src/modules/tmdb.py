import urllib.parse
import urllib.request
import json
import sys
import codecs
import os
import ast

# webAPIからJSONの形式の文字列の結果をもらう


class Tmdb():

    @classmethod
    def dataGet(cls, query):

        # 映画タイトルに字幕、吹替、IMAXが入っている場合はTrue
        def _isInMovieInfo(target):
            word = ['字幕', '吹替', 'IMAX']
            for w in word:
                if w in target:
                    return True
            return False

        def _ejectBrackets(target):
            ret = target
            if _isInMovieInfo(target):
                target_ary = target.split('（')
                title_option = '（' + target_ary[len(target_ary) - 1]
                ret = target.replace(title_option, '')

            return ret

        # URIスキーム
        url = 'https://api.themoviedb.org/3/search/movie?'

        # URIパラメータのデータ
        param = {
            "api_key": os.environ['TMDB_API_KEY'],
            "language": "ja-JP",
            "query": _ejectBrackets(query),
            "page": "1",
            "include_adult": "false"
        }

        # URIパラメータの文字列の作成
        # type=json&user=tamago324_pad と整形される
        paramStr = urllib.parse.urlencode(param)

        # 読み込むオブジェクトの作成
        readObj = urllib.request.urlopen(url + paramStr)

        decodedData = readObj.read().decode('utf-8')
        response = json.loads(decodedData)

        return response
