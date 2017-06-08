# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RetailersItem(scrapy.Item):
    # define the fields for your item here like:
    store_hours = scrapy.Field()
    phone_number = scrapy.Field()
    store_name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    suburb = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
