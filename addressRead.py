import json, ast
from pprint import pprint
import os

path = '/home/ubuntu/gitRepoEVD/.ethereum/keystore/'
#with open('/home/ubuntu/gitRepoEVD/.ethereum/keystore/UTC--2019-05-12T20-02-47.401922532Z--46fde097e9a4aa6eee4b10f217b38bd8f45f3964') as f:
#    data = json.load(f)

#ast.literal_eval(json.dumps(data))

#pprint(data['address'].encode('ascii'))
for r, d, f in os.walk(path):
	for file in f:
		#print(file)
		with open('/home/ubuntu/gitRepoEVD/.ethereum/keystore/'+file) as fopen:
			data = json.load(fopen)
		ast.literal_eval(json.dumps(data))
		#pprint(data['address'].encode('ascii'))
		print(data['address'])

