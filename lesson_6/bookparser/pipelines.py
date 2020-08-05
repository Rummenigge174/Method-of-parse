# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books_programming

    def process_item(self, item, spider):

        if spider.name == 'labirint':
            item['name'] = item['name'][0]
            if not item['price']:
                del item['price']
                item['price_new'][0] = item['price_new'][0].replace(' ', '')
                item['price_old'][0] = item['price_old'][0].replace(' ', '')
                item['price_new'] = int(item['price_new'][0])
                item['price_old'] = int(item['price_old'][0])
            elif not item['price_new']:
                del item['price_new']
                del item['price_old']
                item['price'][0] = item['price'][0].replace(' ', '')
                item['price'] = int(item['price'][0])
            elif not item['price_old']:
                del item['price_old']
                del item['price_new']
                item['price'][0] = item['price'][0].replace(' ', '')
                item['price'] = int(item['price'][0])

            if not item['rate']:
                item['rate'] = 0
            else:
                item['rate'] = item['rate'][0].replace(',', '.')
                item['rate'] = float(item['rate'][0])
        elif spider.name == 'book24':
            item['name'] = item['name'][0]
            item['author'] = item['author'][0]



            if not item['price_old']:
                del item['price_new']
                del item['price_old']
                item['price'][0] = item['price'][0].replace(' ', '')
                item['price'] = int(item['price'][0])
            elif item['price_old']:
                del item['price']
                item['price_new'][0] = item['price_new'][0].replace(' ', '')
                item['price_new'] = int(item['price_new'][0])
                item['price_old'][0] = item['price_old'][0].replace(' ', '')
                item['price_old'][0] = re.findall(r'\d+', item['price_old'][0])
                item['price_old'] = int(item['price_old'][0][0])

            if item['rate']:
                item['rate'] = item['rate'][0].replace(',', '.')
                item['rate'] = float(item['rate'][0])
            else:
                item['rate'] = 0

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
