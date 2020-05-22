from modules import scrape


class Main():

    @classmethod
    def init(cls):
        sc = scrape.Scrape()
        sc.getData()


Main.init()
