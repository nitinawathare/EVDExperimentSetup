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
def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

w3 = Web3(IPCProvider('/home/nitin14/EVDEthereum/.ethereum/geth.ipc', timeout=100000))
#w31 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

# w31 = Web3(IPCProvider('/home/sourav/test-eth1/geth.ipc', timeout=100000))
# w3 = Web3(IPCProvider('/home/sourav/test-eth2/geth.ipc', timeout=100000))

#deploying sort contract, pass size of array as a argument to the constructor

contract_source_path = '/home/nitin14/NewEVD/cpuheavy.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface = compiled_sol.popitem()
curBlock = w3.eth.getBlock('latest')

w3.miner.start(1)

tx_hash1 = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(50).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':4000000})




contract_source_path = '/home/nitin14/NewEVD/matrixMultiplication.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface = compiled_sol.popitem()
curBlock = w3.eth.getBlock('latest')

tx_hash2 = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(4).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':4000000})



contract_source_path = '/home/nitin14/NewEVD/emptyLoop.sol'
# contract_source_path = '/home/sourav/EVD-Prototype/scripts/contracts/simplestorage.sol'
compiled_sol = compile_source_file(contract_source_path)

contract_id, contract_interface = compiled_sol.popitem()
curBlock = w3.eth.getBlock('latest')


tx_hash3 = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor(1000).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':4000000})



receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
while  receipt3 is None:
    time.sleep(1)
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
blockNumber3 = receipt3['blockNumber']

receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
while  receipt2 is None:
    time.sleep(1)
    receipt2 = w3.eth.getTransactionReceipt(tx_hash2)

blockNumber2 = receipt2['blockNumber']

receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
while  receipt1 is None:
    time.sleep(1)
    receipt1 = w3.eth.getTransactionReceipt(tx_hash1)

blockNumber1 = receipt1['blockNumber']

largestNumber = maximum(blockNumber1,blockNumber2,blockNumber3)


curBlock = w3.eth.getBlock('latest')
while curBlock['number'] < largestNumber + k + 1:
    time.sleep(3)
    curBlock = w3.eth.getBlock('latest')

#print("tx blockNumber", blockNumber, "current blockNumber", curBlock['number'])

receipt1 = w3.eth.getTransactionReceipt(tx_hash1)
receipt2 = w3.eth.getTransactionReceipt(tx_hash2)
receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

address1 = receipt1['contractAddress']
address2 = receipt2['contractAddress']
address3 = receipt3['contractAddress']

print("Address:\nsort:{0}\nmatrix:{1}\nempty:{2}".format(address1,address2,address3))


w3.miner.stop()
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
