import os
import time
from crawler import PttCrawlerMongoDB

page = 100

def main():
    print(1)
    db = PttCrawlerMongoDB(board='Beauty', pages=page)
    # a.timer(3600, 10)
    # os.system('scrapy crawl ptt -a board=EZSoft -a pages=2')
    # os.system('scrapy crawl ptt -a board=Gossiping -a pages=100')
    # os.system('scrapy crawl ptt -a board=Beauty -a pages=100')
    # os.system('scrapy crawl ptt -a board=WomenTalk -a pages=100')
    # os.system('scrapy crawl ptt -a board=C_Chat -a pages=100')


if __name__ == '__main__':
    while 1:
        time.sleep(7200)
        main()
        page = 5
