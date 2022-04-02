# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['salary'] = self.process_salary(item['salary'])
        collection.insert_one(item)
        return item




    def process_salary(self, salary):
        result = {'salary_from': None, 'salary_up_to': None, 'valuta': None}
        if len(salary) == 1 or len(salary) == 0:
            return result
        else:
            tmp_nums = []
            tmp_idx = []
            for j, x in enumerate(salary):
                try:
                    tmp_nums.append(float(x.replace('\xa0', '')))
                except:
                    salary[j] = x.lower().replace(' ', '')
                    tmp_idx.append(j)
            for k in tmp_idx:
                if salary[k].startswith('р'):
                    result['valuta'] = 'рубли'
                    break
            if len(tmp_nums) == 2:
                result['salary_from'] = min(tmp_nums)
                result['salary_up_to'] = max(tmp_nums)
            elif len(tmp_nums) == 1:
                if 'от' in salary:
                    result['salary_from'] = tmp_nums[0]
                else:
                    result['salary_up_to'] = tmp_nums[0]

        return result



