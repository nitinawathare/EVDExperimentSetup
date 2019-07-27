import sys
import time
import pprint

from web3 import *
from solc import compile_source


'''
Parameters for Experiments:

1. 40 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      15       |  ----------  |    250 k     |    224323   | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      3        |  ----------  |    250 k     |    244314   | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      15       |  ----------  |    250 k     |    227908   | 
+------------+---------------+--------------+------------- +-------------+


1. 80 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+--------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  |  Exec. time  |
+------------+---------------+--------------+------------- +-------------+--------------+
|  sort      |      30       |  ----------  |   4 Million  |    Gasused  |  Exec. time  | 
+------------+---------------+--------------+------------- +-------------+--------------+
|  Matrix    |      4        |  ----------  |   4 Million  |    Gasused  |  Exec. time  |
+------------+---------------+--------------+------------- +-------------+--------------+
|  Empty     |      30       |  ----------  |   4 Million  |    Gasused  |  Exec. time  |
+------------+---------------+--------------+------------- +-------------+--------------+


2. 800 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |     150       |  ----------  |   8 Million  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      8        |  ----------  |   8 Million  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |     200       |  ----------  |   8 Million  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+

###################################################
Execution of only Memory based contracts.

1. 40 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      --       |      150     |    250 k     |    237742   | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      7        |  ----------  |    350 k     |    304739   | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      15       |  ----------  |    250 k     |    227908   | 
+------------+---------------+--------------+------------- +-------------+

####################################################
For EVD Experiment


1. 400 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      145      |  ----------  |    4305255   |    4205255  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      6        |  ----------  |    1932171   |    1832171  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      170      |  ----------  |    148003    |    138003   | 
+------------+---------------+--------------+------------- +-------------+


1. 800 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      285      |  ----------  |    7916339   |    7816339  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      8        |  ----------  |    3074063   |    2974063  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      345      |  ----------  |    148003    |    138067   | 
+------------+---------------+--------------+------------- +-------------+


1. 1600 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      540      |  ----------  |    15393554  |    14393554 | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      11       |  ----------  |    5397771   |    5297771  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      660      |  ----------  |    148003    |    138067   | 
+------------+---------------+--------------+------------- +-------------+



Memory Contract

1. 12 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      145      |  ----------  |    4305255   |    4205255  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      6        |  ----------  |    1932171   |    1832171  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      170      |  ----------  |    148003    |    138003   | 
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

k = 4
def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def read_address_file(file_path):
    file = open(file_path, 'r')
    addresses = file.read().splitlines() 
    return addresses

def connectWeb3():
    # w3 = Web3(IPCProvider('/home/nitin14/EVDEthereum/.ethereum/geth.ipc', timeout=100000))
    # w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

    # w31 = Web3(IPCProvider('/home/sourav/test-eth3/geth.ipc', timeout=100000))
    # return Web3(IPCProvider('/home/sourav/test-eth1/geth.ipc', timeout=100000))
    return Web3(IPCProvider('/home/nitin14/EVDSetup/test-eth2/geth.ipc', timeout=100000))

def deploySortContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface1 = compiled_sol.popitem()
    tx_hash = w3.eth.contract(
            abi=contract_interface1['abi'],
            bytecode=contract_interface1['bin']).constructor(35).transact({'txType':"0x2", 'from':account, 'gas':11607685})
    return tx_hash


def deployMatrixContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface2 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface2['abi'],
            bytecode=contract_interface2['bin']).constructor(4).transact({'txType':"0x2", 'from':account, 'gas':11758781})
    return tx_hash

def deployEmptyContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor(4).transact({'txType':"0x2", 'from':account, 'gas':1709158})
    return tx_hash

def deployContracts(w3, account):
    tx_hash1 = deploySortContract(sort_source_path, w3, account)
    tx_hash2 = deployMatrixContract(matrix_source_path, w3, account)
    tx_hash3 = deployEmptyContract(empty_source_path, w3, account)

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

    w3.miner.stop()

    if receipt1 is not None:
        print("sort:{0}".format(receipt1['contractAddress']))

    if receipt2 is not None:
        print("matrix:{0}".format(receipt2['contractAddress']))

    if receipt3 is not None:
        print("empty:{0}".format(receipt3['contractAddress']))

# contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
#sort_source_path = '/home/nitin14/EVDExperimentSetup/cpuheavy.sol'
sort_source_path = '/home/nitin14/EVDExperimentSetup/sortMemory.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'

# contract_source_path = '/home/nitin14/NewEVD/matrixMultiplication.sol'
# contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
#matrix_source_path = '/home/nitin14/EVDExperimentSetup/matrixMultiplication.sol'
matrix_source_path = '/home/nitin14/EVDExperimentSetup/matrixMemory.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'

# contract_source_path = '/home/nitin14/NewEVD/emptyLoop.sol'
# contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
empty_source_path = '/home/nitin14/EVDExperimentSetup/emptyLoop.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'

w3 = connectWeb3()
w3.miner.start(1)
time.sleep(4)
deployContracts(w3, w3.eth.accounts[0])