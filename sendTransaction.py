import sys
import time
import pprint

from web3 import *
from solc import compile_source

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def sendSortTransaction(address):

    
    # contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'

    contract_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'

    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.sort(5).transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})

def sendMatrixTransaction(address):

    
    # contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'

    contract_source_path = '/home/sourav/EVD-Expt/matrixMultiplication.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.multiply().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})

def sendEmptyLoopTransaction(address):

    
    # contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
    contract_source_path = '/home/sourav/EVD-Expt/emptyLoop.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.runLoop().transact({'txType':"0x2", 'from':w3.eth.accounts[0], 'gas':8000000})




print("Starting Transaction Submission")
w3 = Web3(IPCProvider('/home/sourav/test-eth4/geth.ipc', timeout=100000))
w3.miner.start(1)

curBlock = w3.eth.getBlock('latest')
while curBlock['number'] < 10:
    time.sleep(1)
    curBlock = w3.eth.getBlock('latest')


i=0
curBlock = w3.eth.getBlock('latest')
while curBlock['number'] < 5000:
#while i < 2:
    with open('contractAddressList') as fp:
        for line in fp:
            #print(line)
            a,b = line.rstrip().split(':', 1)
            if a=="sort":
                sendSortTransaction(b)
            if a=="matrix":
                sendMatrixTransaction(b)
            if a=="empty":  
                sendEmptyLoopTransaction(b) 
            time.sleep(0.08)

    
    #time.sleep(0.08)
    if i%100==0:
        curBlock = w3.eth.getBlock('latest')
    i=i+1


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


w3.miner.stop()
