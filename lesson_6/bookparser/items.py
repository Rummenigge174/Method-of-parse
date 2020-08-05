# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_new = scrapy.Field()
    price_old = scrapy.Field()
    author = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()

