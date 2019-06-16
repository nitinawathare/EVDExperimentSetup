from web3 import Web3, HTTPProvider, IPCProvider
import json
import pprint
import requests
from random import randint
import time

rpcport = '1876'

# # Instantiate web3
w3 = Web3(HTTPProvider('http://127.0.0.1:' + rpcport))
session = requests.Session()

w3 = Web3(IPCProvider('/home/sourav/test-eth3/geth.ipc', timeout=100000))

monitoredOpcode = [
	'CREATE',
	'CALL',
	'CALLCODE',
	'DELEGATECALL'
]

returnOp = [
	'RETURN',
	'SUICIDE'
]

highesetBlockNumber = w3.eth.getBlock('latest').number
startBlockNumber = 0
endBlockNumber = highesetBlockNumber

interval = 100
start = int(startBlockNumber/interval)
end = int(endBlockNumber/interval) + 1

for i in range(start, end):
	# file = open('/home/sourav/EVD-Expt/callChain/Data/callChain'+str(i)+"txt","w+")

	currentStart = i*interval+1
	currentEnd = (i+1)*interval+1
	if currentEnd > endBlockNumber:
		currentEnd = endBlockNumber + 1

	for blockHeight in range(currentStart, currentEnd):
		
		block = w3.eth.getBlock(i, full_transactions=True)
		transactions = block.transactions
		print("+++++++++++++++ Block Number:",blockHeight,"+++++++++++++++")
		
		for txn in transactions:
			_to = txn['to']
			_hash = txn['hash'].hex()

			if (_to is not None) and (w3.eth.getCode(_to).hex() == '0x'):
				# Transaction to a externally owned account.
				continue

			method = 'debug_traceTransaction'
			params = [_hash]
			payload= {
				"jsonrpc":"2.0",
			    "method":method,
			    "params":params,
			    "id":1
			}
			headers = {'Content-type': 'application/json'}

			try:
				rpc_error = False
				debugTraceTransaction = requests.post(
					'http://127.0.0.1:'+rpcport,
					json=payload,
					headers=headers
				)
			except requests.exceptions.RequestException:
				print("JSON-RPC error! hash: ", _hash, blockHeight)

			
			transactionTrace = debugTraceTransaction.json()
			if 'result' in transactionTrace:
				transactionTrace = transactionTrace['result']['structLogs']
			else:
				print('hash: ', _hash, 'No trace available')
				continue

			if transactionTrace:
				logIndex = 0
				logLength = len(transactionTrace)

				while logIndex < logLength:
					log = transactionTrace[logIndex]
					opcode = log['op']
					if opcode == "CREATE":
						print("CREATE Called")
					elif opcode == "CALL": 
						print("CALL Called")
					elif opcode == "DELEGATECALL":
						print("DELEGATECALL Called")
					elif opcode == "CALLCODE":
						print("CALLCODE Called")
					logIndex=logIndex+1
					# else:
						# print(blockHeight, _hash, opcode)	



		# file.write(str(blockHeight)+","+blockHash.hex()+","+str(miner)+"\n")
	# file.close()