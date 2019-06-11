# coding:utf-8

import scrapy
# from scrapy.conf import settings
# from scrapy.selector import Selector
from ptt_crawl.items import PttCrawlItem
from datetime import datetime
# import jieba as jb


def ptt_filter(limits, text):
    if not limits:
        return True
    if limits[0] == '+':
        for lim in limits[1:]:
            if lim in text:
                return True
        return False
    else:  # -
        for lim in limits[1:]:
            if lim in text:
                return False
        return True


class PttSpiderByPage(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    now_pages = 0

    def __init__(self, *args, **kwargs):
        # settings['MONGODB_DOC'] = kwargs['board']
        super(PttSpiderByPage, self).__init__(*args, **kwargs)
        self.item = PttCrawlItem()
        self.item['board'] = kwargs['board']
        self.start_urls = ['https://www.ptt.cc/bbs/%s/index.html' %
                           (kwargs['board'])] if 'board' in kwargs.keys() else []
        self.title_lim = kwargs['title_lim'].split(
            ',')[0:-1] if 'title_lim' in kwargs.keys() else []
        self.MAX_PAGES = int(
            kwargs['pages']) if 'pages' in kwargs.keys() else 1
        # jb.set_dictionary('dict/dict.txt')
        # jb.load_userdict('dict/ptt_dict.txt')

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], cookies={'over18': '1'})

    def parse(self, resp):
        self.now_pages += 1
        print('Now at %s, page #%d' %
              (str(resp).split(' ')[1][:-2], self.now_pages))

        for arti in resp.xpath('//div[@class="r-ent"]/div[@class="title"]/a'):
            # get title
            title = arti.xpath('text()').extract()[0]
            # get url
            url = resp.urljoin(arti.xpath('@href').extract()[0])

            # check title limit
            if ptt_filter(self.title_lim, title):
                print('Parsing: %s\t%s' % (title, url))
                yield scrapy.Request(url=url, cookies={'over18': '1'}, callback=self.parse_post)
            else:
                print('Exclude: %s\t%s' % (title, url))

        if self.now_pages < self.MAX_PAGES:
            # goto next page
            next_page = resp.xpath(
                '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
            if next_page:
                url = resp.urljoin(next_page[0].extract())
                yield scrapy.Request(url=url, cookies={'over18': '1'}, callback=self.parse)

    def parse_post(self, resp):
        # into main-content node
        sel = resp.xpath('//div[@id="main-content"]')

        # get title
        try:
            self.item['title'] = resp.xpath(
                '//meta[@property="og:title"]/@content').get()
        except IndexError:
            self.item['title'] = 'err'

        try:
            # get category
            self.item['category'] = 'Re' if 'Re:' in self.item['title'] \
                else self.item['title'].split(']')[0][1:].strip()
        except IndexError:
            self.item['category'] = 'err'
        except TypeError:
            self.item['category'] = 'err'

        # get author, date
        try:
            # [0]: author, [1]: board, [2]: title [3]: date
            data = sel.css('.article-meta-value::text').getall()
            self.item['author'] = data[0].split()[0]
            self.item['date'] = datetime.strptime(
                data[3], '%a %b %d %H:%M:%S %Y')
        except IndexError:
            self.item['author'] = 'err'
            self.item['date'] = datetime.strptime(
                'Mon Jan 1 00:00:00 1980', '%a %b %d %H:%M:%S %Y')

        # get text
        # split: date, '※ 發信站: 批踢踢實業坊'
        # date = data[3] if len(data) > 3 else 'zzzzzzz'
        # self.item['text'] = ' '.join(sel.xpath('//text()').getall()).split(date)[-1].split('※ 發信站: 批踢踢實業坊')[0]
        # self.item['text'] = ' '.join(jb.cut(self.item['text']))
        # get image link
        self.item['img_link'] = []
        for link in sel.xpath('./a/@href').getall():
            tmp = link.split('.')[-1]  # check it is image, get data type
            if tmp in ['jpg', 'png', 'gif']:
                link.replace('https', 'http')
                self.item['img_link'].append(link)
            elif 'imgur' in link:
                tmp = 'http://i.imgur.com/' + link.split('/')[-1]
                tmp += '.jpg'
                self.item['img_link'].append(tmp)

        # get ip
        # for f2 in sel.xpath('./span[@class="f2"]/text()').getall():
            # if '※ 發信站: 批踢踢實業坊(ptt.cc), 來自:' in f2:
                # self.item['ip_author'] = f2.split(':')[2]
                # break

        # get comment, score
        # comment = []
        # score = 0
        # score_dic = {'推': 1, '噓': -1, '→': 0}
        # for com in sel.xpath('//div[@class="push"]'):
        #     tag = com.css('.push-tag::text').get().strip()
        #     score += score_dic[tag]
        #     user = com.css('.push-userid::text').get().split()[0].strip()
        #     text = com.css('.push-content::text').get().strip(': ')
        #     ip = com.css('.push-ipdatetime::text').get().strip()
        #     ip = ip.split(' ')[0] if '.' in ip else ''
        #     comment.append({'tag': tag, 'user': user, 'text': text, 'ip': ip})

        self.item['url'] = resp.url.strip()
        # self.item['comment'] = comment
        # self.item['score'] = score
        yield self.item
