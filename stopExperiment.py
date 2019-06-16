import sys
import time
import pprint

from web3 import *
# w3 = Web3(IPCProvider('/home/sourav/test-eth4/geth.ipc', timeout=100000))
w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))
# w3.miner.stop()

# time.sleep(30)
file1 = open('/home/ubuntu/gitRepoEVD/minersInChain',"w")
# file1 = open('/home/sourav/minersInChain'+str(i),"w")  
highestBlock = w3.eth.getBlock('latest')
highestBlock = highestBlock['number']
for blockHeight in range(0,highestBlock+1):
    block =  w3.eth.getBlock(blockHeight)
    txns = block['transactions']
    numTxns = len(txns)
    miner = block['miner']
    blockHash = block['hash']
    gasLimit = block['gasLimit']
    gasUsed = block['gasUsed']
    file1.write(str(blockHeight)+","+str(blockHash.hex())+","+str(miner)+","+str(numTxns)+","+str(gasLimit)+","+str(gasUsed)+"\n")
file1.close()