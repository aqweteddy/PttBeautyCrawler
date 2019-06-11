# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
import jieba as jb
import jieba.analyse
import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



class MongoDBPipeline:
    def open_spider(self, spider):
        """
        pyMongo initialize
        """
        client = pymongo.MongoClient(
            host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        tdb = client[settings['MONGODB_DB']]
        self.cur_article = tdb[settings['MONGODB_DB_ARTICLE']]
        self.cur_logs = tdb[settings['MONGODB_DB_LOGS']]
        self.start_time = datetime.datetime.now()

    def process_item(self, item, spider):
        """
        save data into DB.
        """
        # self.cur_article
        if self.cur_article.find({'url': item['url']}).count() == 0:
            self.cur_article.insert(dict(item))
        else:
            self.cur_article.update({'url': item['url']}, dict(item))
        
    def close_spider(self, spider):
        end_time = datetime.datetime.now()
        val = {
            'start_time': self.start_time,
            'end_time': end_time
        }
        self.cur_logs.insert(val)
