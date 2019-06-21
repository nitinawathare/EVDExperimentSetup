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
|  Total     |               |  ----------  |    250 k     |    xxxxxx   |             |
+------------+---------------+--------------+------------- +-------------+-------------+


1. 40 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | Exec. time  |
+------------+---------------+--------------+------------- +-------------+-------------+
|  sort      |      --       |      150     |    250 k     |    237742   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Matrix    |      7        |  ----------  |    350 k     |    304739   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Empty     |      15       |  ----------  |    250 k     |    227908   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Total     |               |  ----------  |    1000k     |    xxxxxx   |     650     |
+------------+---------------+--------------+------------- +-------------+-------------+

2. 120 Million Block measurement time.
+------------+---------------+--------------+------------- +-------------+-------------+
|  Contract  |  Dep. param   |  Txn. param  |    Gaslimit  |    Gasused  | Exec. time  |
+------------+---------------+--------------+------------- +-------------+-------------+
|  sort      |      300      |  ----------  |    750 k     |    607685   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Matrix    |      12       |  ----------  |    800 k     |    758781   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Empty     |      50       |  ----------  |    750 k     |    709158   |             |
+------------+---------------+--------------+------------- +-------------+-------------+
|  Total     |               |  ----------  |    1000k     |    xxxxxx   |     650     |
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

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def read_address_file(file_path):
    file = open(file_path, 'r')
    addresses = file.read().splitlines() 
    return addresses

def connectWeb3():
    return Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=75000))

def deploySortContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface1 = compiled_sol.popitem()
    tx_hash = w3.eth.contract(
            abi=contract_interface1['abi'],
            bytecode=contract_interface1['bin']).constructor(100).transact({'txType':"0x0", 'from':account, 'gas':20000000})
    return tx_hash

def deployMatrixContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface2 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface2['abi'],
            bytecode=contract_interface2['bin']).constructor(8).transact({'txType':"0x0", 'from':account, 'gas':20000000})
    return tx_hash

def deployEmptyContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor(400).transact({'txType':"0x0", 'from':account, 'gas':20000000})
    return tx_hash

def deployContracts(w3, account):
    tx_hash1 = deploySortContract(sort_source_path, w3, account)
    tx_hash2 = deployMatrixContract(matrix_source_path, w3, account)
    tx_hash3 = deployEmptyContract(empty_source_path, w3, account)

    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
    receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    while w3.eth.blockNumber < 10 :
        time.sleep(4)
    time.sleep(30)

    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
    receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    if receipt1 is not None:
        print("sort:{0}".format(receipt1['contractAddress']))

    if receipt2 is not None:
        print("matrix:{0}".format(receipt2['contractAddress']))

    if receipt3 is not None:
        print("empty:{0}".format(receipt3['contractAddress']))


sort_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
# sort_source_path = '/home/ubuntu/gitRepoEVD/sortMemory.sol'

matrix_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
# matrix_source_path = '/home/ubuntu/gitRepoEVD/matrixMemory.sol'

empty_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'


w3 = connectWeb3()
w3.miner.start(1)
deployContracts(w3, w3.eth.accounts[0])
w3.miner.stop()
