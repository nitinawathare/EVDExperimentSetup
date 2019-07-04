''' 
This script calculates the fraction of contract 
which make the nested contract call more than depth 1 
to the total number of contracts
'''


import time
import numpy as np
import matplotlib.pyplot as plt
import os 

filePath = '/home/nitin14/EVD-Scripts/data/'

blockNumberList = []
avgNestedContractList = []
avgTotalContractList=[]
totalTransactionList = []
def computeGasLimit(interval):
	
	
	fileName = ""
	outputFilePath = '/home/nitin14/EVD-Scripts/contractDepth.csv'
	outputFile = open(outputFilePath, "w+")
	outputFile.write("blockHeight,nestedContractTotalRatio,totalContractRatio\n")

	
	nestedContract = 0
	totalContract = 0
	singleDepthContract = 0
	nestedContractTotal = 0
	totalTransactions = 0

	j=1

	for i in range(500,5114):
		
		fileName = filePath+'x'+str(i)+".txt"
		if i==507:
			i=5073
		if i==5113:
			i=6500
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(',')

				blkNumber = int(info[0])
				#totalTransactions = int(info[0])
				#nestedContract = str(int(info[4].split('[')[1]))
				j = j+1

				if j%interval == 0:
					blockNumberList.append(blkNumber)
					avgNestedContractList.append(nestedContractTotal/totalTransactions)
					avgTotalContractList.append(totalContract/totalTransactions)

					avgblkNumber = blkNumber - interval/2
					
					toWrite = str(avgblkNumber)+","+str(nestedContractTotal/totalTransactions)+","+str(totalContract/totalTransactions)+"\n"
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
				#print(str(blkNumber)+" "+str(int(info[2]))+" "+str(int(info[4].split('[')[1]))+" "+str(int(info[5]))+" "+str(int(info[6]))+" "+str(int(info[7]))+" "+str(int(info[8]))+" "+str(int(info[9]))+" "+str(int(info[10]))+" "+str(nestedContract))

				#print(str(blkNumber)+" "+str(totalContract)+" "+str(singleDepthContract)+" "+str(nestedContract))
				# j = j+1

				# if j%interval == 0:
					
				# 	blockNumberList.append(blkNumber)
				# 	emptyBlockFract.append(emptyBlockCount/interval)
				# 	avgblkNumber = blkNumber - interval/2

				# 	toWrite = str(avgblkNumber)+","+str(emptyBlockCount/interval)+","+str(avgGasLimit)+"\n"
				# 	outputFile.write(toWrite)

				# 	emptyBlockCount = 0

				# gasUsed = float(info[6])

				# if gasUsed == 0:
				# 	emptyBlockCount = emptyBlockCount+1

	# outputFile.close()
	# print(blockNumberList)
	# print("*****************************************************")
	# print(emptyBlockFract)


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

computeGasLimit(1000)