import os
import glob

import requests

URI = 'http://127.0.0.1:8000'

data = list()
PATTERN = 'sample/test-*.tif'
files = glob.glob(PATTERN)
for file in files:
    filename = os.path.basename(file)
    body = open(file, 'rb')
    data.append(('projections', (filename, body)))

r = requests.post(URI+'/api/v1/datasets/', params={'name': 'test'}, files=data)
print (r.text)
