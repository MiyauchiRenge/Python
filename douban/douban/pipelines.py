# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs,json,csv,os
import pymongo
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem




class doubanPipeline(object):
    def __init__(self):
        self.file = codecs.open('douban.json', 'a', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    def get_media_requests(self, item, info):
        yield Request(item['image'])

class MongoPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]
    def process_item(self,item,spider):
        self.db[item.collection].insert(dict(item))
        return item
    def close_spider(self,spider):
        self.client.close()
class CSVPipeline(object):
    def process_item(self, item, spider):
        file_path=os.getcwd() + '\\'+'data.csv'
        with open(file_path, 'a+', encoding='GB18030', newline='') as f:
            if os.path.getsize(file_path)==0:
                csv.writer(f, dialect="excel").writerow(('title','rate','movie_url','image','info'))
                csv.writer(f,dialect="excel").writerow((item['title'],item['rate'],item['movie_url'],item['image'],item['info']))
            else:
                csv.writer(f,dialect="excel").writerow((item['title'],item['rate'],item['movie_url'],item['image'],item['info']))
        return item
