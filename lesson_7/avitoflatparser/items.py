# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item
from scrapy.loader.processors import MapCompose, TakeFirst
import re

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    else:
        return value


def cleaner_address(value):
    value = value.replace('\n', '')
    return value


def cleaner_price(value):
    value = int(value.replace(' ', ''))
    return value


def cleaner_name(value):
    value = value.replace('/', "|")
    return value


def cleaner_values(value):
    if value != ' ':
        value = value.replace('\xa0', ' ')
        return value
    del value


def create_dict(params, values):
    if values != ' ':
        values = values.replace('\xa0', ' ')
    else:
        values.popitem()
    parametrs = dict(zip(params, values))
    return parametrs

def cleaner_id(value):
    value = re.findall(r'\d+', value)
    return value


class AvitoflatparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(input_processor=MapCompose(cleaner_id), output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(cleaner_name), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    address = scrapy.Field(input_processor=MapCompose(cleaner_address), output_processor=TakeFirst())
    district = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(cleaner_price), output_processor=TakeFirst())
    body = scrapy.Field(output_processor=TakeFirst())
    parameters = scrapy.Field(output_processor=TakeFirst())
