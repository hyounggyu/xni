import requests

URI = 'http://127.0.0.1:8000'

r = requests.get(URI+'/v1/dataset')
print (r.text)


r = requests.get(URI+'/v1/dataset/')
print (r.text)
