''' Note : Here you mat have to rename the data folder accordingly '''
'''This script calulates the fraction of blocks mined by miner in the main chain and expected number of block mined by a miner present in the main chain based on his mining power'''

import time
import numpy as np
import matplotlib.pyplot as plt
import os 


filePath = '/home/nitin14/EVD-Scripts/goEthereum'

mainChainBlockList = []
miningInfoList = []
plotMainChainBlockList = []
plotMiningInfoList = []
plotExecutionTime = []
plotExpectedBlocks = []
def computeFairness(gas):
	fileName = filePath+str(gas)+'M/Mc/'+str(0)+".dat"
	#print(fileName)
	

	if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(',')
				#print(str(info[1]))
				mainChainBlockList.append(info[1])

	print("*************************************")
	fileName = filePath+str(gas)+'M/Mi/'+str(0)+".dat"
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
	plotMiningInfoList.append(count)
	plotExpectedBlocks.append(0.3302*len(mainChainBlockList))

	toWrite = str(len(mainChainBlockList))+","+str(count)+","+str(0.3302*len(mainChainBlockList))+","

	fileName = filePath+str(gas)+'M/Ex/'+str(0)+".txt"
	#print(fileName)
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

gasList = [240,800]
for gas in gasList:
	computeFairness(gas)