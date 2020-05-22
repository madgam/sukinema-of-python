from modules import scrape, delete


class Main():

    @classmethod
    def init(cls):
        delete.Delete.delete()
        sc = scrape.Scrape()
        sc.getData()


Main.init()
