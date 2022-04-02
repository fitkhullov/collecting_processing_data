import json

import requests as rq
from bs4 import BeautifulSoup as bs
import json
import re

vac = input('Введите интересующую вакансию: ')
url = 'https://novosibirsk.hh.ru'
params = {'cluster': 'true',
          'area': 4,
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'text': vac.replace(' ', '+'),
          'page': 0}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}

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

# Парсим поле с зарплатой в словарь из полей min_salary, max_salary, valuta
for i, vac in enumerate(vac_list):
    salary_row = vac['salary']
    min_val = None
    max_val = None
    valuta = None
    if salary_row is None:
        pass
    else:
        tmp_list = re.split('-| ', salary_row)
        tmp_nums = []
        tmp_idx = []
        for j, x in enumerate(tmp_list):
            try:
                tmp_nums.append(float(x))
            except:
                tmp_list[j] = x.lower()
                tmp_idx.append(j)
        for k in tmp_idx:
            if tmp_list[k].startswith('р'):
                valuta = 'рублей'
                break
        if len(tmp_nums) == 2:
            min_val = min(tmp_nums)
            max_val = max(tmp_nums)
        elif len(tmp_nums) == 1:
            if 'от' in tmp_list:
                min_val = tmp_nums[0]
            else:
                max_val = tmp_nums[0]

    vac_list[i]['salary'] = {'min_salary': min_val, 'max_salary': max_val, 'valuta': valuta}

with open('vacancies.json', 'w') as f:
    f.write(json.dumps(vac_list, ensure_ascii=False))
