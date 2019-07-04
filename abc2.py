from web3 import Web3, HTTPProvider, IPCProvider
import json
import pprint
import requests
from random import randint
import time

rpcport = '21000'

# Instantiate web3
web3 = Web3(HTTPProvider('http://localhost:' + rpcport))

session = requests.Session()

#latest = web3.eth.getTransactionFromBlock("late)
#transactions = web3.eth.getBlock(7584952)["transactions"]

#NumberOfTransactionsInBlock= open("NumberOfTransactionsInBlock.txt","w+")
#gasLimitGasUsed = open("gasLimitGasUsed.txt","w+")
#for latest in web3.eth.getBlock(7584952)["transactions"]:
#       print (latest.hex());

#blockHeight = 7585283
for index in range(60,75):
        counter = 61000
        previous = 60000
        while counter <=70000:
                lower = index*100000 + 1 + previous
                upper = index*100000 + 1 + counter
                NumberOfTransactionsInBlockFileName = "{0}/{1}_{2}.{3}".format("/ssd/data2","NumberOfTransactionsInBlock",index*100000+1+previous,"txt")
                gasLimitGasUsedFileName  = "{0}/{1}_{2}.{3}".format("/ssd/data2","gasLimitGasUsed",index*100000+1+previous,"txt")
                print(lower, upper)
                print(NumberOfTransactionsInBlockFileName, gasLimitGasUsedFileName)
                NumberOfTransactionsInBlock= open(NumberOfTransactionsInBlockFileName,"w+")
                gasLimitGasUsed = open(gasLimitGasUsedFileName,"w+")
                for blockHeight in range(lower, upper):
                        block = web3.eth.getBlock(blockHeight)
                        blockTrans = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}\n".format(block["number"],block["hash"].hex(),len(block["transactions"]), block["size"],block["difficulty"],block["gasLimit"],block["gasUsed"], block["timestamp"])
                        NumberOfTransactionsInBlock.write(blockTrans)
                        #print(blockTrans)
                        for latest in block["transactions"]:

                                instr = "{0}, {1}, {2}, {3}\n".format(blockHeight,latest.hex(), web3.eth.getTransaction(latest.hex())["gas"], web3.eth.getTransactionReceipt(latest.hex())["gasUsed"])
                                gasLimitGasUsed.write(instr)

                NumberOfTransactionsInBlock.close()
                gasLimitGasUsed.close()
                previous = counter
                counter=counter+1000

