from web3 import Web3, HTTPProvider, IPCProvider
import json
import pprint
import requests
from random import randint
import time

rpcport = '21000'

# # Instantiate web3
w3 = Web3(HTTPProvider('http://127.0.0.1:' + rpcport))
session = requests.Session()

monitoredOpcode = [
	'CREATE',
	'CALL',
	'CALLCODE',
	'DELEGATECALL',
	'STATICCALL'
]

returnOp = [
	'RETURN',
	'SUICIDE',
	'SELFDESTRUCT',
	'REVERT',
	'STOP'
]

startBlockNumber =  5006549
endBlockNumber =  w3.eth.getBlock('latest').number

interval = 10000
start = int(startBlockNumber/interval)
end = int(endBlockNumber/interval) + 1


for i in range(start, end):
	file = open('/ssd/callChain/data/x'+str(i)+".txt","a+")

	currentStart = i*interval+1
	if currentStart < startBlockNumber:
		currentStart = startBlockNumber
	currentEnd = (i+1)*interval+1
	if currentEnd > endBlockNumber:
		currentEnd = endBlockNumber + 1

	for blockHeight in range(currentStart, currentEnd):
		
		block = w3.eth.getBlock(blockHeight, full_transactions=True)
		txns = block.transactions

		numTxns = len(txns)
		numContractTxns = 0
		numUnprocessedTxns = 0
		blkTotalCallCounts = [0]*1024

		for txn in txns:
			_to = txn['to']
			_hash = txn['hash'].hex()
			_receipt = w3.eth.getTransactionReceipt(_hash)
			_gasUsed = _receipt['gasUsed']

			if _gasUsed > 1000000:
				continue
			if _hash == "0xa6e0f880ca60af058a28b5b4266b9f88ca7eeb3967cb9e44e254ed6c4deec351":
				continue

			# Checking whether the transaction is to a EOA or not.
			if (_to is not None) and (w3.eth.getCode(_to).hex() == '0x'):
				# print(_hash, "EOA")
				continue

			numContractTxns = numContractTxns + 1 
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
				debugTraceTransaction = requests.post(
					'http://127.0.0.1:'+rpcport,
					json=payload,
					headers=headers
				)
			except requests.exceptions.RequestException:
				numUnprocessedTxns = numUnprocessedTxns + 1
				print("JSON-RPC error! hash: ", _hash, blockHeight)
				continue
			
			transactionTrace = debugTraceTransaction.json()
			if 'result' in transactionTrace:
				transactionTrace = transactionTrace['result']['structLogs']
			else:
				print('hash: ', _hash, 'No trace available')
				continue				

			if transactionTrace:
				logIndex = 0
				logLength = len(transactionTrace)

				callQueue = []
				callDepth = 0
				maxCallDepth = 0
				currentContract = _to

				while logIndex < logLength:
					log = transactionTrace[logIndex]
					opcode = log['op']

					if opcode == "CREATE":
						callQueue.append(currentContract)
						currentContract = "CREATECALL"
						# print("CREATE Called")

					elif (opcode == "CALL") or (opcode == "STATICCALL") or (opcode == "DELEGATECALL") or (opcode == "CALLCODE"):
						callQueue.append(currentContract)
						calleeAddrees = log['stack'][-2][24:]
						callDepth = callDepth + 1
						if callDepth > maxCallDepth:
							maxCallDepth = callDepth
						currentContract = calleeAddrees
						# print(opcode, "CALLED")

					elif (opcode == "RETURN") or (opcode == "STOP") or (opcode == "SELFDESTRUCT") or (opcode == "SUICIDE") or (opcode == "REVERT"):
						if callQueue:
							if currentContract == "CREATECALL":
								# contractAddress = transactionTrace[logIndex+1]['stack'][-1][24:]
								currentContract = callQueue.pop(-1)
							else:
								currentContract = callQueue.pop(-1)
								callDepth = callDepth - 1
						
					if(logIndex + 1 == logLength):
						blkTotalCallCounts[maxCallDepth] = blkTotalCallCounts[maxCallDepth]+1
						# print(opcode, "Called")

					logIndex=logIndex+1
		file.write(str(blockHeight)+","+str(numTxns)+","+str(numContractTxns)+","+str(numUnprocessedTxns)+","+str(blkTotalCallCounts)+"\n")
	file.close()
