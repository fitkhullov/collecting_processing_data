import json

import requests as rq
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json

vac = input('Введите интересующую вакансию: ')
url = 'https://novosibirsk.hh.ru'
params = {'cluster': 'true',
          'area': 4,
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'text': vac.replace(' ', '+'),
          'page': 0}
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}

vac_list = []
while True:
    response = rq.get(url + '/search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    if response.ok and vacancies:
        for vacancy in vacancies:
            vac_data = {}
            info = vacancy.find('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
            name = vacancy.find('a', {'class': 'bloko-link'}).text
            link = info.find('a', {'class': 'bloko-link'})['href']
            try:
                salary = info.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
                salary = salary.replace('\u202f', '')
            except:
                salary = None

            homepage = url
            vac_data['name'] = name
            vac_data['link'] = link
            vac_data['salary'] = salary
            vac_data['homepage'] = homepage
            vac_list.append(vac_data)
        print(f'Страница №{params["page"]} обработана')
        params['page'] += 1
    else:
        break

with open('vacancies.json', 'w') as f:
    f.write(json.dumps(vac_list, ensure_ascii=False))

