from web3 import Web3, HTTPProvider, IPCProvider
import json
import pprint
import requests
from random import randint
import time

rpcport = "21000"
_hash = "0x1731f15ab76e21c374f5d9e4b55cb6392558354dce41ae63565425b708cff9d2"
method = 'debug_traceTransaction'
params = [_hash]
payload= {
	"jsonrpc":"2.0",
    "method":method,
    "params":params,
    "id":1
}
headers = {'Content-type': 'application/json'}

print("Trying RPC")
try:
	debugTraceTransaction = requests.post(
		'http://132.145.209.11:'+rpcport,
		json=payload,
		headers=headers
	)
except requests.exceptions.RequestException:
	print("JSON-RPC error! hash: ", _hash)
print("Established Connection")