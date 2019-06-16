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

    
    contract_source_path = '/home/ubuntu/gitRepoEVD/cpuheavy.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/cpuheavy.sol'

    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.sort(5).transact({'from':w3.eth.accounts[0], 'gas':4000000})

def sendMatrixTransaction(address):

    
    contract_source_path = '/home/ubuntu/gitRepoEVD/matrixMultiplication.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/matrixMultiplication.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.multiply().transact({'from':w3.eth.accounts[0], 'gas':4000000})

def sendEmptyLoopTransaction(address):

    
    contract_source_path = '/home/ubuntu/gitRepoEVD/emptyLoop.sol'
    # contract_source_path = '/home/sourav/EVD-Expt/emptyLoop.sol'
    compiled_sol = compile_source_file(contract_source_path)

    contract_id, contract_interface = compiled_sol.popitem()

    sort_contract = w3.eth.contract(
    address=address,
    abi=contract_interface['abi'])
    tx_hash = sort_contract.functions.runLoop().transact({'from':w3.eth.accounts[0], 'gas':4000000})




print("Starting Transaction Submission")
# w3 = Web3(IPCProvider('/home/sourav/test-eth4/geth.ipc', timeout=100000))
w3 = Web3(IPCProvider('/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc', timeout=100000))

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

            if i%100==0:
                curBlock = w3.eth.getBlock('latest')
            i=i+1

w3.miner.stop()

time.sleep(30)
file1 = open('/home/ubuntu/gitRepoEVD/minersInChain',"w")
highestBlock = w3.eth.getBlock('latest')
highestBlock = highestBlock['number']
for blockHeight in range(0,highestBlock+1):
    block =  w3.eth.getBlock(blockHeight)
    miner = block['miner']
    blockHash = block['hash']
    file1.write(str(blockHeight)+","+blockHash.hex()+","+str(miner)+"\n")
file1.close()