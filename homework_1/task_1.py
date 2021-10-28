import requests as rq
import json

username = 'fitkhullov'
url = f'https://api.github.com/users/{username}/repos'
repos = {'Names': []}

j_data = rq.get(url).json()

for i in range(len(j_data)):
    repos['Names'].append(j_data[i]['name'])

with open('repos_names.json', 'w') as fp:
    fp.write(json.dumps(repos))
