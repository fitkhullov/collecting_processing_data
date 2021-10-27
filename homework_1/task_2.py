import requests as rq
import json
from pprint import pprint

url = 'https://api.github.com/user'
token = ''
name = 'fitkhullov'

s = rq.post(url, auth=(name, token))

if s.ok:
        print(f'Аутентификация пройдена')
else:
        print(f'Аутентификация не пройдена. Status Code = {s.status_code}')