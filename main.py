import os
from crawler import PttCrawlerMongoDB


def main():
    print(1)
    db = PttCrawlerMongoDB(board='Beauty', pages=10)
    # a.timer(3600, 10)
    # os.system('scrapy crawl ptt -a board=EZSoft -a pages=2')
    # os.system('scrapy crawl ptt -a board=Gossiping -a pages=100')
    # os.system('scrapy crawl ptt -a board=Beauty -a pages=100')
    # os.system('scrapy crawl ptt -a board=WomenTalk -a pages=100')
    # os.system('scrapy crawl ptt -a board=C_Chat -a pages=100')


if __name__ == '__main__':
    main()
