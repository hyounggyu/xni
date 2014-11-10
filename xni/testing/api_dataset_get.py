import requests

URI = 'http://127.0.0.1:8000'

r = requests.get(URI+'/api/v1/datasets/')
print (r.text)
