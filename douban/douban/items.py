# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class doubanItem(scrapy.Item):
    collection='douban'
    title = scrapy.Field()
    rate = scrapy.Field()
    movie_url = scrapy.Field()
    image = scrapy.Field()
    info=scrapy.Field()
