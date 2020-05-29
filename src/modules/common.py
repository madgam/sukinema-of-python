
class Common():

    @classmethod
    def cleansing(cls, target):

        s = target.replace('\u3000', ' ')
        s = s.replace('\xa0', '')
        s = s.replace('(', '（')
        s = s.replace(')', '）')

        return s.strip()

    @classmethod
    def createValuesQuery(cls, sql_values, id, title, pref, theater, latitude, longitude, description, link, time, all_time, review, release_date, drop_path, poster_path):

        movie = (id, title, pref, theater, latitude, longitude, description,
                 link, time, all_time, review, release_date, drop_path, poster_path)

        sql_values.append(movie)
