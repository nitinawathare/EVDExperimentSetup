import sys
import time
import pprint

from web3 import *
from solc import compile_source


'''
Parameters for Experiments:

1. 400 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      160      |  ----------  |    2809638   |    2372157  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      6        |  ----------  |    2409638   |    2095287  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      170      |  ----------  |    2409638   |    2359158  | 
+------------+---------------+--------------+------------- +-------------+

1. 500 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | 
+------------+---------------+--------------+------------- +-------------+
|  sort      |      180      |  ----------  |    3209638   |    2372157  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      6        |  ----------  |    2409638   |    2095287  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |      170      |  ----------  |    2409638   |    2359158  | 
+------------+---------------+--------------+------------- +-------------+


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
|  sort      |     150       |  ----------  |   5.5 M      |    5121763  | 
+------------+---------------+--------------+------------- +-------------+
|  Matrix    |      8        |  ----------  |   4.5 M      |    4487369  | 
+------------+---------------+--------------+------------- +-------------+
|  Empty     |     400       |  ----------  |   6.0 M      |    5521658  | 
+------------+---------------+--------------+------------- +-------------+



###################################################
Execution of only Memory based contracts.

0. 12 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | Exec. time  |
+------------+---------------+--------------+------------- +-------------+-------------+
|  sort      |      30       |  ----------  |    75 k      |    67264    |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Matrix    |      4        |  ----------  |    75 k      |    57681    |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Empty     |      4        |  ----------  |    100 k     |    76658    |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Total     |               |  ----------  |    250 k     |    xxxxxx   |    1750     |
+------------+---------------+--------------+------------- +-------------+-------------+

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

2. 120 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | Exec. time  |
+------------+---------------+--------------+------------- +-------------+-------------+
|  sort      |      300      |  ----------  |    250 k     |    607685   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Matrix    |      12       |  ----------  |    350 k     |    758781   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Empty     |      50       |  ----------  |    250 k     |    709158   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Total     |               |  ----------  |    1000 k    |    xxxxxx   |    1750     |
+------------+---------------+--------------+------------- +-------------+-------------+

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



def maximum(a, b, c): 
  
    if (a >= b) and (a >= b): 
        largest = a 
  
    elif (b >= a) and (b >= a): 
        largest = b 
    else: 
        largest = c 
          
    return largest


k = 10
def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def read_address_file(file_path):
    file = open(file_path, 'r')
    addresses = file.read().splitlines() 
    return addresses


def connectWeb3():
    # w3 = Web3(IPCProvider('/home/nitin14/EVDSetup/.ethereum/geth.ipc', timeout=100000))
    # w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

    # w31 = Web3(IPCProvider('/home/sourav/test-eth3/geth.ipc', timeout=100000))
    return Web3(IPCProvider('/home/nitin14/EVDSetup/test-eth1/geth.ipc', timeout=100000))
    # w3 = Web3(IPCProvider('/home/sourav/test-eth2/geth.ipc', timeout=100000))

def deploySortContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface1 = compiled_sol.popitem()
    tx_hash = w3.eth.contract(
            abi=contract_interface1['abi'],
            bytecode=contract_interface1['bin']).constructor(145).transact({'txType':"0x0", 'from':account, 'gas':8500000})
    return tx_hash


def deployMatrixContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface2 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface2['abi'],
            bytecode=contract_interface2['bin']).constructor(6).transact({'txType':"0x0", 'from':account, 'gas':4000000})
    return tx_hash

def deployEmptyContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor(170).transact({'txType':"0x0", 'from':account, 'gas':1000000})
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

    w3.miner.stop()

    if receipt1 is not None:
        print("sort:{0}".format(receipt1['contractAddress']))

    if receipt2 is not None:
        print("matrix:{0}".format(receipt2['contractAddress']))

    if receipt3 is not None:
        print("empty:{0}".format(receipt3['contractAddress']))


sort_source_path = '/home/nitin14/EVDExperimentSetup/cpuheavy.sol'
#sort_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'
#sort_source_path = '/home/sourav/EVD-Expt/sortMemory.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'

matrix_source_path = '/home/nitin14/EVDExperimentSetup/matrixMultiplication.sol'
# contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
# matrix_source_path = '/home/sourav/EVD-Expt/matrixMultiplication.sol'
#matrix_source_path = '/home/sourav/EVD-Expt/matrixMemory.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'

# contract_source_path = '/home/nitin14/NewEVD/emptyLoop.sol'
# contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
empty_source_path = '/home/nitin14/EVDExperimentSetup/emptyLoop.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'

w3 = connectWeb3()
w3.miner.start(1)
time.sleep(4)
deployContracts(w3, w3.eth.accounts[0])