# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider, Request
from urllib.parse import urlencode
from douban.items import doubanItem
import time
from scrapy import Selector

class doubanMovieSpider(scrapy.Spider):
    name = 'douban_movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']


    def start_requests(self):
        base_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&'
        for page in range(0,17):
            time.sleep(3)
            pages='page_start={}'.format(page*20)
            url = base_url + pages
            yield Request(url, self.parse)



    def parse(self, response):
        result = json.loads(response.text)
        for movie in result.get('subjects'):
            item=doubanItem()
            item['rate']=movie['rate']
            item['title']=movie['title']
            item['image']=movie['cover']
            item['movie_url']=movie['url']
            request = scrapy.Request(url=movie['url'],
                                     callback=self.parse_page)
            request.meta['item'] = item

            yield request

    def parse_page(self, response):
        #子页xpath应用
        item = response.meta['item']
        result1=response.xpath('//div[@id="link-report"]//span/text()').getall()
        info = ';'.join(result1)
        item['info'] = info
        yield item





