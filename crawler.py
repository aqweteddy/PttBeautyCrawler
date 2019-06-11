import os
from ptt_crawl import settings
import pymongo
import time
# from datetime import datetime
# import urllib


class PttCrawlerBase:
    FOLDER = os.path.split(os.path.realpath(__file__))[0]

    def __init__(self, board='Gossiping', pages=1, file=None, title_lim=None):
        """
        :param board: board
        :param pages: crawled page
        :param file: output's json file_name.
        :param title_lim: set title limit.
        """

        # crawl
        com = 'scrapy crawl ptt '
        # output json file name
        if file:
            com += '-o {} '.format(file)
        # page
        com += '-a pages={:d} '.format(pages)
        # board
        com += '-a board={} '.format(board)

        # title limit
        if title_lim:
            com += '-a title_lim="'
            for lim in title_lim:
                com += "%s," % (str(lim))
            com += '" '
        self.com = com
        # start spider
        print('command: {}'.format(com))
        os.system(com)

    def timer(self, sec, times):
        """
        :param sec: time interval between every crawl task.
        :param times: how many times do you want to crawl?
        :return: No
        """
        for i in range(times):
            print('command: {}'.format(self.com))
            os.system(self.com)
            time.sleep(sec)


class PttCrawlerMongoDB(PttCrawlerBase):
    def __init__(self, board='Gossiping', pages=1, title_lim=None, only_connect_db=False):
        if not only_connect_db:
            super(PttCrawlerMongoDB, self).__init__(board=board, pages=pages, file=None, title_lim=title_lim)
        # MongoDB
        client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        self.__db = client[settings.MONGODB_DB]
        self.article = self.__db.article
        self.user = self.__db.user

    def find(self, col, dic, show=None):
        if col not in ('article', 'user'):
            raise KeyError('Error collection name. Need "article" or "user"')
        return list(self.__db[col].find(dic, show))

    def filter(self, col, match, cond, show):
        """
        use mongoDB aggressive()
        select all match data (match::dict)
        only return match cond(cond::dict) data
        :param col::str: select collection
        :param match::dict: select data from db.
        :param cond::dict: in match case, return data according to cond. use variable data to represent a document.
        :param show::tuple: selecting row need to return
        :return: cursor
        ex: PttCrawlMongoDB.filter('user', {"id": "XXX"}, {'$eq': ['$$data.board', 'Beauty']}, ('id', 'ip'))
        In collection 'user', find all of id:XXX post, return the post which matchhing data.board == Beauty,
        show two property.
        """
        if col not in ('article', 'user'):
            raise KeyError('Error collection name. Need "article" or "user"')

        project = {
            'data': {
                '$filter': {
                    'input': '$data',
                    'as': 'data',
                    'cond': cond
                }
            }
        }
        for it in show:
            project[it] = 1
        print(project)
        pipeline = [
            {"$match": match},
            {"$project": project}
        ]
        return self.__db[col].aggregate(pipeline)


class PttCrawlerJson(PttCrawlerBase):
    def __init__(self, board='Gossiping', pages=1, title_lim=None, file='tmp.json', save_db=False):
        if not save_db:
            settings.ITEM_PIPELINES = []
        super(PttCrawlerJson, self).__init__(board=board, pages=pages, file=file, title_lim=title_lim)


def main():
    # a = PttCrawlerMongoDB(only_connect_db=True)
    # print(a.find('a', {
    #     'id': 'wglhe'
    # }))
    #
    a = PttCrawlerMongoDB(board='Gossiping', pages=5)
    # a.timer(600, 10)
    result = a.filter('user', {"id": "curtis7248"}, {'$eq': ['$$data.board', 'Beauty']}, ('id', 'ip'))
    print(result)
    # for it in result:
    #    print(it)
    # start = datetime(2019, 2, 5, 0, 0, 0)
    # end = datetime(2019, 2, 6, 0, 0, 0)
    # for item in a.find({'date': {'$lt': end, '$gt': start}}):
    #     print(item['title'], item['date'])
    #


if __name__ == '__main__':
    # a = CrawlerToolBox(board='Gossiping', pages=10)
    main()
