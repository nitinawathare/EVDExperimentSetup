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
	'DELEGATECALL'
]

returnOp = [
	'RETURN',
	'SUICIDE',
	'SELFDESTRUCT'
]

highesetBlockNumber = w3.eth.getBlock('latest').number
# startBlockNumber = highesetBlockNumber-100
# endBlockNumber = highesetBlockNumber-50
startBlockNumber =  7858420
endBlockNumber =  7858421

interval = 100
start = int(startBlockNumber/interval)
end = int(endBlockNumber/interval) + 1


# def updateTxnTotalCallCounts(txnTotalCallCounts, contractAddress, callDepth):
# 	if calleeAddrees in txnTotalCallCounts:
# 		callDepths = txnTotalCallCounts[calleeAddrees]
# 		if callDepth in callDepths:
# 			callDepths[callDepth] = callDepths[callDepth] + 1
# 		else:
# 			callDepths[callDepth] = 1
# 	else:
# 		txnTotalCallCounts[calleeAddrees] = {callDepth:1}

# def updateBlkTotalCallCounts(blkTotalCallCounts, contractAddress, callDepth):
# 	if calleeAddrees in blkTotalCallCounts:
# 		callDepths = blkTotalCallCounts[calleeAddrees]
# 		if callDepth in callDepths:
# 			callDepths[callDepth] = callDepths[callDepth] + 1
# 		else:
# 			callDepths[callDepth] = 1
# 	else:
# 		blkTotalCallCounts[calleeAddrees] = {callDepth:1}

def updateOtherCallCounts(logIndex, logLength, blkOtherCallCounts, txnOtherCallCounts, callDepth, currentContract, createdAddresses, callQueue):
	if logIndex == logLength-1:
		while callDepth >= 0:
			if currentContract not in createdAddresses:
				txnOtherCallCounts[callDepth] = txnOtherCallCounts[callDepth] + 1
				blkOtherCallCounts[callDepth] = blkOtherCallCounts[callDepth] + 1
			callDepth = callDepth-1
			if callQueue:
				currentContract = callQueue.pop(-1)
	else:
		if currentContract not in createdAddresses:
			txnOtherCallCounts[callDepth] = txnOtherCallCounts[callDepth] + 1
			blkOtherCallCounts[callDepth] = blkOtherCallCounts[callDepth] + 1

def updateTotalCallCounts(logIndex, logLength, blkTotalCallCounts, callDepth, currentContract, callQueue):
	if logIndex == logLength-1:
		while callDepth >= 0:
			blkTotalCallCounts[callDepth] = blkTotalCallCounts[callDepth]+1
			callDepth = callDepth-1
			if callQueue:
				currentContract = callQueue.pop(-1)
	else:
		blkTotalCallCounts[callDepth] = blkTotalCallCounts[callDepth]+1

#---------------------------------------

for i in range(start, end):
	file = open('/home/ubuntu/callChain/Data/callChain'+str(i)+".txt","w")

	currentStart = i*interval+1
	currentEnd = (i+1)*interval+1
	if currentEnd > endBlockNumber:
		currentEnd = endBlockNumber + 1

	currentStart =  7858420
	currentEnd =  7858421

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
						print("CREATE Called")

					elif (opcode == "CALL") or (opcode == "STATICCALL") or (opcode == "DELEGATECALL") or (opcode == "CALLCODE"):
						callQueue.append(currentContract)
						calleeAddrees = log['stack'][-2][24:]
						callDepth = callDepth + 1
						if callDepth > maxCallDepth:
							maxCallDepth = callDepth
						currentContract = calleeAddrees
						print(opcode, "CALLED")

					elif (opcode == "RETURN") or (opcode == "STOP") or (opcode == "SELFDESTRUCT") or (opcode == "SUICIDE") or (opcode == "REVERT"):
						if callQueue:
							if currentContract == "CREATECALL":
								contractAddress = transactionTrace[logIndex+1]['stack'][-1][24:]
								currentContract = callQueue.pop(-1)
							else:
								currentContract = callQueue.pop(-1)
								callDepth = callDepth - 1
						
					if(logIndex + 1 == logLength):
						blkTotalCallCounts[maxCallDepth] = blkTotalCallCounts[maxCallDepth]+1
						print(opcode, "Called")


						
						# if currentContract == "CREATECALL":
						# 	if transactionTrace[logIndex+1] is not None:
						# 		contractAddress = transactionTrace[logIndex+1]['stack'][-1][24:]
						# 		if contractAddress not in createdAddresses:
						# 			createdAddresses.append(contractAddress)
						# 		currentContract = callQueue.pop(-1)
						# else:
						# 	blkTotalCallCounts[callDepth] = blkTotalCallCounts[callDepth]+1
						# 	if callQueue:
						# 		if currentContract not in createdAddresses:
						# 			txnOtherCallCounts[callDepth] = txnOtherCallCounts[callDepth] + 1
						# 			blkOtherCallCounts[callDepth] = blkOtherCallCounts[callDepth] + 1
						# 		currentContract = callQueue.pop(-1)
						# 	callDepth = callDepth - 1
							
						# file.write("RETURN,\t"+currentContract+",\t"+str(callDepth)+"\n")
						# print("RETURN Called")

					# elif opcode == "SELFDESTRUCT":
					# 	callDepth = callDepth-1
					# 	if callQueue:
					# 		currentContract = callQueue.pop(-1)
					# 	updateOtherCallCounts(logIndex, logLength, blkOtherCallCounts, txnOtherCallCounts, callDepth, currentContract, createdAddresses, callQueue)
					# 	updateTotalCallCounts(logIndex, logLength, blkTotalCallCounts, callDepth, currentContract, callQueue)
					# 	# # file.write("SELFDESTRUCT,\t"+currentContract+",\t"+str(callDepth)+"\n")
					# 	print("SELFDESTRUCT Called")

					# elif opcode == "SUICIDE":
					# 	callDepth = callDepth-1
					# 	if callQueue:
					# 		currentContract = callQueue.pop(-1)
					# 	updateOtherCallCounts(logIndex, logLength, blkOtherCallCounts, txnOtherCallCounts, callDepth, currentContract, createdAddresses, callQueue)
					# 	updateTotalCallCounts(logIndex, logLength, blkTotalCallCounts, callDepth, currentContract, callQueue)
					# 	# # file.write("SUICIDE,\t"+currentContract+",\t"+str(callDepth)+"\n")
					# 	print("SUICIDE Called")

					# elif opcode == "REVERT":
					# 	callDepth = callDepth-1
					# 	if callQueue:
					# 		currentContract = callQueue.pop(-1)
					# 	updateOtherCallCounts(logIndex, logLength, blkOtherCallCounts, txnOtherCallCounts, callDepth, currentContract, createdAddresses, callQueue)
					# 	updateTotalCallCounts(logIndex, logLength, blkTotalCallCounts, callDepth, currentContract, callQueue)
					# 	# # file.write("REVERT,\t"+currentContract+",\t"+str(callDepth)+"\n")
					# 	print("REVERT Called")

					logIndex=logIndex+1
		file.write(str(blockHeight)+","+str(numTxns)+","+str(numContractTxns)+","+str(numUnprocessedTxns)+","+str(blkTotalCallCounts)+"\n")
	file.close()