# -*- coding: utf-8 -*-
import scrapy
import json

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['https://image.so.com/zjl?ch=photography&sn=30&listtype=new&temp=1']

    def start_requests(self):
        base_url = 'https://image.so.com/zjl?ch=photography&sn={}&listtype=new&temp=1'
        for page in range(1,self.settings['MAX_PAGE']+1):
            url = base_url.format(page*30)
            yield scrapy.Request(
                url,
                callback=self.parse
            )
    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = {}
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            yield item