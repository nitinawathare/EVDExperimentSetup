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


######################################################
Memory based Execution.

3. 240 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | Exec. time  |
+------------+---------------+--------------+------------- +-------------+-------------+
|  sort      |      620      |  ----------  |    1.5 M     |   1315056   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Matrix    |      15       |  ----------  |    1.5 M     |   1423713   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Empty     |      120      |  ----------  |    1.75 M    |   1671658   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Total     |               |  ----------  |              |   xxxxxxx   |     650     |
+------------+---------------+--------------+------------- +-------------+-------------+

'''

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def sendSortTransaction(address):
    contract_source_path = '/home/ubuntu/gitRepoEVD/sortMemory.sol'
    # contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'

    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.sort().transact({'txType':"0x1", 'from':w3.eth.accounts[0], 'gas':75000})

def sendMatrixTransaction(address):
    contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMemory.sol'
    # contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/matrixMultiplication.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.multiply().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':75000})

def sendEmptyLoopTransaction(address):
    contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/emptyLoop.sol'
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.runLoop().transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':100000})

print("Starting Transaction Submission")
# w3 = Web3(IPCProvider('/home/sourav/test-eth4/geth.ipc', timeout=100000))
w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

file = open('/home/ubuntu/gitRepoEVD/experimentTimeStats',"w")
file.write("Experiment Start Time"+str(datetime.datetime.now())+"\n")

w3.miner.start(1)

curBlock = w3.eth.getBlock('latest')
while curBlock['number'] < 10:
    time.sleep(1)
    curBlock = w3.eth.getBlock('latest')


i=0
curBlock = w3.eth.getBlock('latest')
while curBlock['number'] < 2020:
#while i < 2:
    # with open('/home/sourav/contractAddressList1') as fp:
    with open('/home/ubuntu/gitRepoEVD/contractAddressList') as fp:
        for line in fp:
            #print(line)
            a,b = line.rstrip().split(':', 1)
            if a=="sort":
                sendSortTransaction(b)
            if a=="matrix":
                sendMatrixTransaction(b)
            if a=="empty":  
                sendEmptyLoopTransaction(b) 
            time.sleep(0.5)

        curBlock = w3.eth.getBlock('latest')
        file.write(str(curBlock['number'])+","+str(datetime.datetime.now())+"\n")
        
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
