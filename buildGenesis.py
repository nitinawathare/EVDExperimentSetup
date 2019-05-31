import json
from pprint import pprint
import sys

listAcc = {}
#listAcc['0xcf22ddf426fefe909f28fc006689884e10273e5f'] = {"balance": "1000000000000000000000000000"}
#listAcc['0xeefb042c0f799ff2b9836239ef6bcee5b96c41dd'] = {"balance": "10000000000"}

file = open("address.txt", "r") 
list = file.read().splitlines() 
length = len(list) 
for i in range(length): 
        #print(list[i])
        listAcc[list[i]] = {"balance": "10000000000000000000000000000000"}
element = {
          "config": {
            "chainId": 2310,
            "homesteadBlock": 0,
            "eip155Block": 0,
            "eip158Block": 0
            },

            "alloc"      : listAcc,
            "coinbase"   : "0x0000000000000000000000000000000000000000",
            "difficulty" : "0x0",
            "extraData"  : "",
            "gasLimit"   : "0x2FAF0800",
            "gasLimit1"  : "0x3D0900",
            "nonce"      : "0x0000000000000042",
            "mixhash"    : "0x0000000000000000000000000000000000000000000000000000000000000000",
            "parentHash" : "0x0000000000000000000000000000000000000000000000000000000000000000",
            "timestamp"  : "0x00"
            }


json_text = json.dumps(element)
print(json_text)



