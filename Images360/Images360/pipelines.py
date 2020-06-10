# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import scrapy

client = MongoClient()
collection = client['photo']['image360']

class Images360Pipeline(object):
    def process_item(self, item, spider):
        collection.insert(item)
        return item

class ImagePieline(ImagesPipeline):
    #继承scrapy内部的Imagespipeline
    #提取url生成request对象加入调度队列执行下载
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'])
    #修改文件名称
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
    #判断是否下载成功
    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok ,x in results if ok]
        if not image_path:
            raise DropItem('Item Download Failed')
        item['image_path'] = image_path
        return item