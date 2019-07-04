import sys
import time
import pprint

from web3 import *
from solc import compile_source



'''
+------------+--------------+
|  Contract  |    TxType    |
+------------+--------------+
|   Sort     |      1       |
+------------+--------------+
|   Matrix   |      2       |
+------------+--------------+
|   Empty    |      3       |
+------------+--------------+

+------------+--------------+-------------+
|  Contract  |   Parameter  |  Gas used   |
+------------+--------------+-------------+
|   Sort     |      1       |   298092    |
+------------+--------------+-------------+
|   Matrix   |      2       |   182938    |
+------------+--------------+-------------+
|   Empty    |      3       |   227908    |
+------------+--------------+-------------+

'''
def maximum(a, b, c): 
  
    if (a >= b) and (a >= b): 
        largest = a 
  
    elif (b >= a) and (b >= a): 
        largest = b 
    else: 
        largest = c 
          
    return largest

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def sendSortTransaction(address):
    # contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'
    contract_source_path = '/home/sourav/EVD-Expt/sortMemory.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.sort().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':77002})
    return tx_hash

def sendMatrixTransaction(address):
    # contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
    contract_source_path = '/home/sourav/EVD-Expt/matrixMemory.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    matrix_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = matrix_contract.functions.multiply().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':57681})
    return tx_hash

def sendEmptyLoopTransaction(address):
    # contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
    contract_source_path = '/home/sourav/EVD-Expt/emptyLoop.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    empty_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = empty_contract.functions.runLoop().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':76658})
    return tx_hash

print("Starting Transaction Submission")
w3 = Web3(IPCProvider('/home/sourav/test-eth1/geth.ipc', timeout=100000))
# w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

w3.miner.start(1)

i=0
k=4
# curBlock = w3.eth.getBlock('latest')
# while curBlock['number'] < 100:
while i < 1000:
    with open('/home/sourav/EVD-Expt/contractAddressList1') as fp:
    # with open('/home/ubuntu/gitRepoEVD/contractAddressList') as fp:
        for line in fp:
            #print(line)
            a,b = line.rstrip().split(':', 1)
            if a=="sort":
                tx_hash1 = sendSortTransaction(b)
            if a=="matrix":
                tx_hash2 = sendMatrixTransaction(b)
            if a=="empty":  
                tx_hash3 = sendEmptyLoopTransaction(b) 


    
    #time.sleep(0.08)
    # if i%100==0:
        # curBlock = w3.eth.getBlock('latest')
    i=i+1

receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

while ((receipt3 is None) or (receipt2 is None) or (receipt1 is None)) :
    time.sleep(1)
    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
    receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

blkNumber1 = receipt1['blockNumber']
blkNumber2 = receipt2['blockNumber']
blkNumber3 = receipt3['blockNumber']

maxBlkNumber = maximum(blkNumber1, blkNumber2, blkNumber3)
while w3.eth.blockNumber < maxBlkNumber + k +1:
    time.sleep(2)


receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

if receipt1 is not None:
    print("sort:{0}".format(receipt1['gasUsed']))

if receipt2 is not None:
    print("matrix:{0}".format(receipt2['gasUsed']))

if receipt3 is not None:
    print("empty:{0}".format(receipt3['gasUsed']))



w3.miner.stop()
# file1 = open('/home/sourav/EVD-Expt/minersInChain',"w")
# highestBlock = w3.eth.getBlock('latest')
# highestBlock = highestBlock['number']
# for blockHeight in range(0,highestBlock+1):
#     block =  w3.eth.getBlock(blockHeight)
#     miner = block['miner']
#     blockHash = block['hash']
#     file1.write(str(blockHeight)+","+blockHash.hex()+","+str(miner)+"\n")
# file1.close()