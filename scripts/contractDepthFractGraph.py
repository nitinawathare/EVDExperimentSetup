''' 
This script calculates the fraction of contract 
which make the nested contract call more than depth 1 
to the total number of contracts
'''

'''
Organization of Data:

datadir		:	/ssd/callChain/data1
start block :	5,000,001
end block 	:	5,145,039
note		:	All information are available
interval	:	1000


datadir		:	/ssd/callChain/data2
start block :	6,500,000
end block 	:	6,554,960
note		:	All information are available
interval	:	1000

'''

import time
import numpy as np
import matplotlib.pyplot as plt
import os 

filePath = '/ssd/callChain/'


def computeGasLimit65(interval, start, end):
	inputFilePath = filePath+"data2/"
	outputFilePath = "/home/sourav/EVD-Expt/data/contInt65.csv"
	outputFile = open(outputFilePath, "w+")
	outputFile.write("blockHeight,numTxns,numContTxns,numIntContTxn,intContRatio,totalContRatio\n")
	
	computeFraction(interval, start, end, inputFilePath, outputFile)	

def computeGasLimit50(interval, start, end):
	inputFilePath = filePath+"data1/"
	outputFilePath = "/home/sourav/EVD-Expt/data/contInt50.csv"
	outputFile = open(outputFilePath, "w+")
	outputFile.write("blockHeight,numTxns,numContTxns,numIntContTxn,intContRatio,totalContRatio\n")

	computeFraction(interval, start, end, inputFilePath, outputFile)
		

def computeFraction(interval, start, end, inputFilePath, outputFile):
	blockNumberList = []
	avgNestedContractList = []
	avgTotalContractList=[]
	totalTransactionList = []


	nestedContract = 0
	totalContract = 0
	singleDepthContract = 0
	nestedContractTotal = 0
	totalTransactions = 0


	j=0
	for i in range(start, end):
		fileName = inputFilePath+'x'+str(i)+".txt"
		print(fileName)
		
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(',')

				blkNumber = int(info[0])

				j = j+1
				if j%interval == 0:
					blockNumberList.append(blkNumber)
					avgNestedContractList.append(nestedContractTotal/totalTransactions)
					avgTotalContractList.append(totalContract/totalTransactions)

					avgblkNumber = blkNumber - interval/2
					
					print(totalTransactions, totalContract, nestedContractTotal)

					toWrite = str(avgblkNumber)+","+str(totalTransactions/interval)+","+str(totalContract/interval)+","+str(nestedContractTotal/interval)+","+str(nestedContractTotal/totalTransactions)+","+str(totalContract/totalTransactions)+"\n"
					outputFile.write(toWrite)


					nestedContract=0
					totalContract=0
					nestedContractTotal = 0
					totalTransactions = 0

				singleDepthContract = int(info[4].split('[')[1])
				nestedContract = int(info[5])
				for k in range(6,1027):
					nestedContract = nestedContract+int(info[k])

				totalContract = totalContract + int(info[2])	
				totalTransactions = totalTransactions + int(info[1])	
				nestedContractTotal = nestedContractTotal + nestedContract

	plt.figure(1)
	plt.plot(blockNumberList,avgNestedContractList , label='Nested contracts')
	plt.plot(blockNumberList,avgTotalContractList , label='Total contracts')
	plt.title("histogram") 
	plt.grid(True)
	plt.legend(loc="upper left")

	plt.xlabel('Block height')
	plt.ylabel('Number of contracts')
	plt.title('Gas usage and limit with increasing block height')
	plt.show()

# computeGasLimit65(5000,6500,6554)
# computeGasLimit50(5000,5000,5145)