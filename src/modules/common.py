
class Common():

    @classmethod
    def cleansing(cls, target):
        s = target.replace('\u3000', ' ')
        s = s.replace('\xa0', '')
        s = s.replace('(', '（')
        s = s.replace(')', '）')

        return s.strip()
