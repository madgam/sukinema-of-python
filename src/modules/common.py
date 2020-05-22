
class Common():

    @classmethod
    def cleansing(cls, target):
        s = target.replace('\u3000', ' ')
        s = s.replace('\xa0', '')
        s = s.replace('(', '（')
        s = s.replace(')', '）')

        return s.strip()

    @classmethod
    def createValuesQuery(cls, sql_values, title, pref, theater, latitude, longitude, description, link, time, all_time, review, release_date, drop_path, poster_path):

        movie = {
            'title': title,
            'pref': pref,
            'theater': theater,
            'latitude': str(latitude),
            'longitude': str(longitude),
            'description': description,
            'link': link,
            'time': time,
            'all_time': all_time,
            'review': str(review),
            'release_date': release_date,
            'drop_path': drop_path,
            'poster_path': poster_path
        }

        sql_values.append(
            '(' + ', '.join(['\'' + str(v) + '\'' for v in movie.values()]) + ')')
