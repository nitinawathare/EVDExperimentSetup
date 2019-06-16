import sys
import time
import pprint

from web3 import *
from solc import compile_source




def maximum(a, b, c): 
  
    if (a >= b) and (a >= b): 
        largest = a 
  
    elif (b >= a) and (b >= a): 
        largest = b 
    else: 
        largest = c 
          
    return largest


k = 10

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

'''

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

# w3 = Web3(IPCProvider('/home/nitin14/EVDEthereum/.ethereum/geth.ipc', timeout=100000))
w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

# w31 = Web3(IPCProvider('/home/sourav/test-eth3/geth.ipc', timeout=100000))
# w3 = Web3(IPCProvider('/home/sourav/test-eth3/geth.ipc', timeout=100000))
# w3 = Web3(IPCProvider('/home/sourav/test-eth2/geth.ipc', timeout=100000))

#deploying sort contract, pass size of array as a argument to the constructor


contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
# contract_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface1 = compiled_sol.popitem()
curBlock = w3.eth.getBlock('latest')

w3.miner.start(1)
tx_hash1 = w3.eth.contract(
        abi=contract_interface1['abi'],
        bytecode=contract_interface1['bin']).constructor(15).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})




# contract_source_path = '/home/nitin14/NewEVD/matrixMultiplication.sol'
contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface2 = compiled_sol.popitem()
curBlock = w3.eth.getBlock('latest')

tx_hash2 = w3.eth.contract(
        abi=contract_interface2['abi'],
        bytecode=contract_interface2['bin']).constructor(3).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})



# contract_source_path = '/home/nitin14/NewEVD/emptyLoop.sol'
contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'

# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface3 = compiled_sol.popitem()
curBlock = w3.eth.getBlock('latest')


tx_hash3 = w3.eth.contract(
        abi=contract_interface3['abi'],
        bytecode=contract_interface3['bin']).constructor(15).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})


while w3.eth.blockNumber < 10 :
    time.sleep(4)
w3.miner.stop()

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


# address1 = receipt1['contractAddress']
# address2 = receipt2['contractAddress']
# address3 = receipt3['contractAddress']

# print("sort:{0}\nmatrix:{1}\nempty:{2}".format(address1,address2,address3))


# sort_contract = w3.eth.contract(
#    address=address1,
#    abi=contract_interface1['abi'])


# matrix_contract = w3.eth.contract(
#    address=address2,
#    abi=contract_interface2['abi'])


# empty_contract = w3.eth.contract(
#    address=address3,
#    abi=contract_interface3['abi'])


# for i in range(0,2):
#     tx_hash11 = sort_contract.functions.sort(400).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':25000000})
#     tx_hash21 = matrix_contract.functions.multiply().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':10000000})
#     tx_hash31 = empty_contract.functions.runLoop().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':1500000})
#     time.sleep(0.8)
#     if (i+1)%10==0:
#         print("Submitted",i,"transaction")


# receipt11 = w3.eth.getTransactionReceipt(tx_hash11)
# receipt21 = w3.eth.getTransactionReceipt(tx_hash21)
# receipt31 = w3.eth.getTransactionReceipt(tx_hash31)


# while (receipt11 is None) or (receipt21 is None) or (receipt31 is None):
#     receipt11 = w3.eth.getTransactionReceipt(tx_hash11)
#     receipt21 = w3.eth.getTransactionReceipt(tx_hash21)
#     receipt31 = w3.eth.getTransactionReceipt(tx_hash31)
#     time.sleep(1)    

# gu1 = receipt11['gasUsed']
# gu2 = receipt21['gasUsed']
# gu3 = receipt31['gasUsed']

# print("Address:\nsort:{0}\nmatrix:{1}\nempty:{2}".format(gu1,gu2,gu3))

# time.sleep(10)

# w31.miner.stop()

# curBlock = w3.eth.getBlock('latest')
# while curBlock['number'] < 10:
#     time.sleep(1)
#     curBlock = w3.eth.getBlock('latest')
# w3.miner.stop()

'''sort_contract = w3.eth.contract(
   address=address,
   abi=contract_interface['abi'])

# gas_estimate = store_var_contract.functions.setVar(255).estimateGas()
# print("Gas estimate to transact with setVar: {0}\n".format(gas_estimate))

print("Starting Transaction Submission")

i=0
curBlock = w3.eth.getBlock('latest')
while curBlock['number'] < 5000:
    tx_hash = sort_contract.functions.set(5).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})
    time.sleep(0.08)
    if i%100==0:
        curBlock = w3.eth.getBlock('latest')
    i=i+1

# for i in range(0,100):
#     tx_hash = sort_contract.functions.set(5).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})
#     time.sleep(0.8)
#     if (i+1)%10==0:
#         print("Submitted",i,"transaction")

# w3.miner.start(1)
# receipt = w3.eth.getTransactionReceipt(tx_hash)
# while  receipt is None:
#     time.sleep(1)
#     receipt = w3.eth.getTransactionReceipt(tx_hash)
# w3.miner.stop()

# blockNumber = receipt['blockNumber']

# curBlock = w3.eth.getBlock('latest')
# w3.miner.start(1)
# while curBlock['number'] < blockNumber + k:
#     time.sleep(3)
#     curBlock = w3.eth.getBlock('latest')
# w3.miner.stop()
# print(sort_contract.functions.get().call())




receipt = w3.eth.getTransactionReceipt(tx_hash)
while  receipt is None:
    time.sleep(1)
    receipt = w3.eth.getTransactionReceipt(tx_hash)
# w3.miner.stop()

blockNumber = receipt['blockNumber']
curBlock = w3.eth.getBlock('latest')
# w3.miner.start(1)
while curBlock['number'] < blockNumber + k:
    time.sleep(3)
    curBlock = w3.eth.getBlock('latest')

''
w3.miner.stop()'''
# print(sort_contract.functions.get("hello").call())
# print(sort_contract.functions.get("world").call())


# receipt = w3.eth.getTransactionReceipt(tx_hash)
# print("Transaction receipt mined: \n")
# pprint.pprint(dict(receipt))
