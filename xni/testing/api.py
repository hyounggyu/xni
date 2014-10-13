import time

import requests

import params

URI = 'http://127.0.0.1:8000'

r = requests.post('http://127.0.0.1:8000/api/v1/tasks/shift/', params.params)
print(r.status_code, r.text)

for _ in range(30):
    r = requests.get('http://127.0.0.1:8000/api/v1/tasks/status.json')
    print(r.status_code, r.text)
    time.sleep(1)

#r = requests.post('{}/api/v1/path/files/'.format(URI), {
#    'pattern': '/IU*'
#})

#print(r.status_code, r.text)

#r = requests.post('{}/api/v1/path/directory/'.format(URI), {
#    'directory': '/'
#})

#print(r.status_code, r.text)

#r = requests.post('{}/api/v1/path/directory/'.format(URI), {
#    'directory': '/IU'
#})

#print(r.status_code, r.text)

