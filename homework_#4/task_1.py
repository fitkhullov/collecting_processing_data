import requests as rq
from lxml import html
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/95.0.4638.69 Safari/537.36'}

url = 'https://yandex.ru/news/'

response = rq.get(url, headers=header)

dom = html.fromstring(response.text)

link_and_text = dom.xpath('//div[contains(@class, "mg-grid__col_xs")]//a[@class="mg-card__link"]')
source_and_time = dom.xpath('//div[contains(@class, "mg-grid__col_xs")]//div[@class="mg-card-footer__left"]')
news = []

# Сбор данных

for x, y in zip(link_and_text, source_and_time):
    name = x.xpath('./h2/text()')[0].replace('\xa0', ' ')
    link = x.xpath('./@href')[0]
    source = y.xpath('.//a[@class="mg-card__source-link"]/text()')[0]
    time = y.xpath('.//span[@class="mg-card-source__time"]/text()')[0].split(' ')
    k = 0 if len(time) == 1 else 1  # если новость вчерашняя, то нужно будет отнять единицу из номера текущего дня
    hour_time = int(time[-1][:2])
    minute_time = int(time[-1][3:])
    current_date = datetime.now()
    current_date = {'year': current_date.year, 'month': current_date.month, 'day': current_date.day - k,
                    'hour': hour_time, 'minute': minute_time}
    tmp = {'source': source, 'name': name, 'link': link, 'post_time': current_date}
    news.append(tmp)

# Загрузка данных в MongoDB

ip = '127.0.0.1'
port = 27017

client = MongoClient(ip, port)

db = client['yandex_news']
news_collection = db.news

if news_collection.count_documents({}) == 0:
    for x in news:
        news_collection.insert_one(x)
else:
    for x in news:
        if not news_collection.find_one({'link': x['link']}):
            news_collection.insert_one(x)
