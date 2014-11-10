import requests

URI = 'http://127.0.0.1:8000'

r = requests.delete(URI+'/api/v1/datasets/', params={'name': 'test'})
print (r.text)
