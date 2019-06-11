# PttScrapyMongoDB

## Environment

1. MacOS Sierra

## Usage

### Preparation

1. install mongoDB server.
2. `pip install -r requirements.txt`

### Command line

* in project folder
* run command in shell:  
    `scrapy crawl ptt -a board=EZSoft -a pages=2`
    1. board: boardName
    2. pages: the number of crawling page.
    3. title_lim

### Class

#### PttCrawlerMongoDB

#### PttCrawlerMongoJson


### other function

1. timer spider

## MongoDBPortSettings

*  ptt_crawl/spiders/settings.py

```python
ITEM_PIPELINES = {
    'ptt_crawl.pipelines.MongoDBPipeline': 300
}

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "ptt"
MONGODB_DOC = "ptt"
```

## Log

### V0.2 2019.2.10

1. rewrite xpath
2. use pipeline to save data into MongoDB.
3. fix bug: can't crawl all text in article.
4. Performance improvement: the crawl time decreases.

### V0.1 2019.2.1

1. initial version