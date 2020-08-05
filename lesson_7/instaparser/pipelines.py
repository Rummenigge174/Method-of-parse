# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import re

# class DataBasePipeline:
#
#
#
# class AvitoPhotosPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         if item['photo']:
#             for img in item['photo']:
#                 try:
#                     yield scrapy.Request(img, meta=item)
#                 except Exception as e:
#                     print(e)
#
#     def file_path(self, request, response=None, info=None):
#         item = request.meta
#         return f'{item["fullname"]}/'+os.path.basename(urlparse(request.url).path)
#
#     def item_completed(self, results, item, info):
#         if results:
#             item['photo'] = [itm[1] for itm in results if itm[0]]
#         return item



class InstaparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.insta_followers

    def process_item(self, item, spider):
        i=0
        j=0
        try:
            collection = self.mongo_base[spider.name]
            collection.insert_one(item)
            i += 1
            return item
        except (DuplicateKeyError):
            j += 1
        # print(f'Загружено {i}')
        # print(f'Попытка загрузить дубликат {j}')

    def __del__(self):
        self.client.close()