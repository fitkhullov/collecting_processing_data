from pymongo import MongoClient
from pprint import pprint

gt_salary = float(input('Введите интересуемую зарплату: '))

ip = '127.0.0.1'
port = 27017

client = MongoClient(ip, port)

db = client['HH']
vacancies = db.vacancies

interest_vacancies = vacancies.find({'$or': [{'min_salary': {'$gt': gt_salary}}, {'max_salary': {'$lt': gt_salary}}]},
                                    {'_id': False, 'name': True})

for x in interest_vacancies:
    pprint(x['name'])
