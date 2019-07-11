''' Note : Here you mat have to rename the data folder accordingly '''
'''This script calulates the fraction of blocks mined by miner in the main chain and expected number of block mined by a miner present in the main chain based on his mining power'''

import time
import numpy as np
import matplotlib.pyplot as plt
import os 


filePath = '/home/nitin14/EVD-Segate/ETH-NS-ND-HET/'

mainChainBlockList = []
miningInfoList = []
plotMainChainBlockList = []
plotMiningInfoList = []
plotExecutionTime = []
plotExpectedBlocks = []
plotGasLimit = []
def computeFairness(gas):
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Het/Mc/'+str(0)+".dat"
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Homo/Mc/'+str(0)+".dat"
	fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Het/Mc/'+str(0)+".dat"
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-XX-Homo/Mc/'+str(0)+".dat"
	#fileName = filePath+"ETH-"+str(gas)+'-Skip-1x/Mc/'+str(0)+".dat"
	#fileName = filePath+"EVD800_"+str(gas)+'xDelay/Mc/'+str(0)+".dat"
	#fileName = filePath+"EVD"+str(gas)+'/Mc/'+str(0)+".dat"
	#fileName = filePath+"EVD-"+str(gas)+'-Skip-1x/Mc/'+str(0)+".dat"
	print(fileName)
	

	if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(',')
				#print(str(info[1]))
				mainChainBlockList.append(info[1])

	print("*************************************")
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Het/Mi/'+str(0)+".dat"
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Homo/Mi/'+str(0)+".dat"
	fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Het/Mi/'+str(0)+".dat"
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-XX-Homo/Mi/'+str(0)+".dat"
	#fileName = filePath+"ETH-"+str(gas)+'-Skip-1x/Mi/'+str(0)+".dat"
	#fileName = filePath+"EVD800_"+str(gas)+'xDelay/Mi/'+str(0)+".dat"
	#fileName = filePath+"EVD"+str(gas)+'/Mi/'+str(0)+".dat"
	#fileName = filePath+"EVD-"+str(gas)+'-Skip-1x/Mi/'+str(0)+".dat"
	
	print(fileName)
	if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(' ')
				#print(str(info[0]))
				miningInfoList.append(info[0])

	count = 0
	for line in miningInfoList:
		if line in mainChainBlockList:
			count = count+1
	print(str(count) +" : "+str(len(mainChainBlockList))+" : "+str(0.3302*len(mainChainBlockList)))
	plotMainChainBlockList.append(len(mainChainBlockList))
	plotMiningInfoList.append(count/len(mainChainBlockList))
	plotExpectedBlocks.append(0.3302*len(mainChainBlockList)/len(mainChainBlockList))
	plotGasLimit.append(gas)
	toWrite = str(len(mainChainBlockList))+","+str(count)+","+str(0.3302*len(mainChainBlockList))+","

	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Het/Ex/'+str(0)+".txt"
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Homo/Ex/'+str(0)+".txt"
	fileName = filePath+"ETH-"+str(gas)+'-NoSkip-1x-Het/Ex/'+str(0)+".txt"
	#fileName = filePath+"ETH-"+str(gas)+'-NoSkip-XX-Homo/Ex/'+str(0)+".txt"
	#fileName = filePath+"ETH-"+str(gas)+'-Skip-1x/Ex/'+str(0)+".txt"
	#fileName = filePath+"EVD800_"+str(gas)+'xDelay/Ex/'+str(0)+".txt"
	#fileName = filePath+"EVD"+str(gas)+'/Ex/'+str(0)+".txt"
	#fileName = filePath+"EVD-"+str(gas)+'-Skip-1x/Ex/'+str(0)+".txt"
	
	print(fileName)
	count = 0
	sumExTime = 0
	avgExTime = 0
	if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(' ')
				#print(info[7])
				sumExTime = sumExTime+float(info[7])
				count = count+1
	print(str(sumExTime/count))			
	plotExecutionTime.append(sumExTime/count)
	print("*************************************")

	toWrite = toWrite+str(sumExTime/count)+"\n"
	outputFile.write(toWrite)
					

	mainChainBlockList.clear()
	miningInfoList.clear()


outputFilePath = '/home/nitin14/EVD-Scripts/ethereumFairnessGraph.csv'
outputFile = open(outputFilePath, "w+")
outputFile.write("totalMainchainBlock,minerMainChainBlock,expectedBlocks,avgExecutionTime\n")

gasList = [40,800]
#gasList = [40,400,800]
for gas in gasList:
	computeFairness(gas)

print(plotExpectedBlocks)
print(plotMiningInfoList)
print(plotGasLimit)


plt.figure(1)
plt.scatter(plotGasLimit,plotMiningInfoList , label='Actual blocks in main chain')
plt.scatter(plotGasLimit, plotExpectedBlocks, label='Expected blocks in main chain')
plt.title("histogram") 
plt.grid(True)
plt.legend(loc="upper left")

plt.xlabel('Gas Limit')
plt.ylabel('Fraction of Blocks in main chain')
plt.title('Gas Limit and Number of Blocks in main chain EVD-S-D')
plt.show()
