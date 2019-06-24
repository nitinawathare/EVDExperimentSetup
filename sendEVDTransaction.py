import sys
import time
import pprint

from web3 import *
from solc import compile_source
import datetime



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

1. 40 Million Gas limit
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      15       |  ----------  |    250 k     |    224323   | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      3        |  ----------  |    250 k     |    244314   | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      15       |  ----------  |    250 k     |    227908   | 
+------------+---------------+--------------+------------- +-------------+

2. 800 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |     150       |  ----------  |   5.5 M      |    5121763  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      8        |  ----------  |   4.5 M      |    4487369  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |     400       |  ----------  |   6.0 M      |    5521658  | 
+------------+---------------+--------------+------------- +-------------+

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
    contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/sortMemory.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.sort().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':350000})
    return tx_hash

def sendMatrixTransaction(address):
    contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/matrixMultiplication.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/matrixMemory.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    matrix_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = matrix_contract.functions.multiply().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':350000})
    return tx_hash

def sendEmptyLoopTransaction(address):
    contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/emptyLoop.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    empty_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = empty_contract.functions.runLoop().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':350000})
    return tx_hash

print("Starting Transaction Submission")
# w3 = Web3(IPCProvider('/home/sourav/test-eth1/geth.ipc', timeout=100000))
w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

file = open('/home/ubuntu/gitRepoEVD/experimentTimeStats',"w")
file.write("Experiment Start Time"+str(datetime.datetime.now())+"\n")

w3.miner.start(1)

i=0
k=7
# curBlock = w3.eth.getBlock('latest')
while w3.eth.blockNumber < 1050:
# while i < 2000:
    # with open('/home/sourav/EVD-Expt/contractAddressList1') as fp:
    with open('/home/ubuntu/gitRepoEVD/contractAddressList') as fp:
        for line in fp:
            #print(line)
            a,b = line.rstrip().split(':', 1)
            if a=="sort":
                tx_hash1 = sendSortTransaction(b)
            if a=="matrix":
                tx_hash2 = sendMatrixTransaction(b)
            if a=="empty":  
                tx_hash3 = sendEmptyLoopTransaction(b) 
            # time.sleep(0.01)
        file.write(str(w3.eth.blockNumber)+","+str(datetime.datetime.now())+"\n")

    #time.sleep(0.08)
    # if i%100==0:
        # curBlock = w3.eth.getBlock('latest')
    i=i+1

blkNumber = w3.eth.blockNumber
while w3.eth.blockNumber < blkNumber + k +1:
    time.sleep(2)

w3.miner.stop()
        
time.sleep(30)
file1 = open('/home/ubuntu/gitRepoEVD/minersInChain',"w")
highestBlock = w3.eth.getBlock('latest')
highestBlock = highestBlock['number']
for blockHeight in range(0,highestBlock+1):
    block =  w3.eth.getBlock(blockHeight)
    miner = block['miner']
    blockHash = block['hash']
    numberOfTransactions = len(block['transactions'])
    gasLimit = block['gasLimit']
    gasUsed = block['gasUsed']

    file1.write(str(blockHeight)+","+blockHash.hex()+","+str(miner)+","+str(numberOfTransactions)+","+str(gasLimit)+","+str(gasUsed)+"\n")
file1.close()
file.close()