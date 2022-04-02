# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from leruaparser.runner import query

class LeruaparserPipeline:
    def __init__(self):
        collection = MongoClient('localhost', 27017)
        self.mongo_base = collection['goods']

    def process_item(self, item, spider):
        collection = self.mongo_base[query]
        if not collection.find_one({'link': item['link']}):
            collection.insert_one(item)
        return item

class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item  # возвращение элемента из текущего pipeline

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = item['photos'].index(request.url)
        return f'{query}/{item["name"]}/full/{image_guid}.jpg'
