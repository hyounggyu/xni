import requests

import api_params

URI = 'http://127.0.0.1:8000'

#r = requests.post('http://127.0.0.1:8000/api/v1/shift/', api_params.params)

r = requests.post('{}/api/v1/path/files/'.format(URI), {
    'pattern': '/IU*'
})

print(r.status_code, r.text)

r = requests.post('{}/api/v1/path/directory/'.format(URI), {
    'directory': '/'
})

print(r.status_code, r.text)

r = requests.post('{}/api/v1/path/directory/'.format(URI), {
    'directory': '/IU'
})

print(r.status_code, r.text)

