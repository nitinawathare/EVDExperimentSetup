'''
'''

import math
import time
import numpy as np
import matplotlib.pyplot as plt
import os 
import sys
from collections import defaultdict

skipFailDict = {
	1:[26,36,23,27,39],
	2:[48,36,27,32,46],
	4:[48,26,28,36,23,32]
}
skipFailAll = [23,26,27,28,32,36,39,48]

noSkipFailDict = {
	1:[16,48,32],
	2:[24,32,36,39,46,48],
	4:[24,28,46]
}
noSkipAll = [16,24,28,32,36,39,46,48]


# Compute the address of the first miner
def firstMinerAddress(inputFilePath, evd = True):
	fileName = inputFilePath+'Mi/0.dat'
	firstMiner = ""
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()
		if evd:
			firstMiner = data[0].rstrip().split(' ')[8]
		else:
			firstMiner = data[0].split(' ')[5]
	return firstMiner

def computeFirstHashPower(inputFilePath, startBlk, endBlk):
	hashPowerAtBlock = {}
	blockHashes = {}
	fileName = inputFilePath+'Mc/0.dat'
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			info = dataItem.split(',')
			blkNum = int(info[0])
			if blkNum < startBlk:
				continue
			elif blkNum > endBlk:
				break
			else:
				blkHash = info[1]
				blockHashes[blkNum] = blkHash
				hashPowerAtBlock[blkNum] = hashPowers[0]
	else:
		print("Error", fileName, "file not found")
	return hashPowerAtBlock

def mainChainHashes(inputFilePath, startBlk, endBlk):
	blockHashes = {}
	fileName = inputFilePath+'Mc/0.dat'
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			info = dataItem.split(',')
			blkNum = int(info[0])
			if blkNum < startBlk:
				continue
			elif blkNum > endBlk:
				break
			else:
				blkHash = info[1]
				blockHashes[blkNum] = blkHash
	else:
		print("Error", fileName, "file not found")
	return blockHashes

def computeNumMinedBlocks(inputFilePath, startBlk, endBlk):
	minedBlocks = {}
	fileName = inputFilePath+'Mc/0.dat'
	totalBlkCount =  0

	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			info = dataItem.split(',')
			blkNum = int(info[0])
			if blkNum < startBlk:
				continue
			elif blkNum > endBlk:
				break
			else:
				totalBlkCount= totalBlkCount + 1
				miner = info[2]
				if minedBlocks.get(miner):
					minedBlocks[miner] = minedBlocks[miner] + 1
				else:
					minedBlocks[miner] = 1
	else:
		print("Error", fileName, "file not found")
	return minedBlocks

# Evd files
# 0xfc125a8af0a01e0e18c34816ce0b6fcf208c762861df1bca9d463662abd8c452 601 166 3500000 3486000 500000000 485867636 485701636 0xbd611E337D54dfdbe9A052Fe689a7486cB59156c

# Eth files
# 0x42c195850143eb25243719fae3a2eb2df1de093520e27bdd7097c64494d3b4e2 456 67 12000000 4707183 0xbd611E337D54dfdbe9A052Fe689a7486cB59156c 1.124s

def computeForkRate(inputFilePath, outputFile, startBlk, endBlk, strategy, delay, evd=True):
	global totalMinedBlocks, chunkMinedBlocks
	minedBlocks = computeNumMinedBlocks(inputFilePath, startBlk, endBlk)
	blockHashes = mainChainHashes(inputFilePath, startBlk, endBlk)
	mainChainRatio = {}

	chunkMinedBlocks = 0
	for i in range(0,49):
		mainChainRatio[i] = 0.0
		# if i in noSkipFailDict[delay]:
		# 	continue

		fileName = inputFilePath+"Mi/"+str(i)+".dat"
		minerBlocks = 0

		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()
			if len(data) == 0:
				# print(fileName, " no data found!!")
				continue
			# print(fileName)
			minerId = ""
			if evd:
				minerId = data[0].rstrip().split(' ')[8]
			else:
				minerId = data[0].rstrip().split(' ')[5]

			print(i,":", end=" ")
			numForkedBlocks = 0 	
			for dataItem in data:
				info = dataItem.split(' ')
				blkNum = int(info[1])
				blockHash = info[0]
				if blkNum < startBlk:
					continue
				elif blkNum > endBlk:
					break
				else:
					totalMinedBlocks = totalMinedBlocks + 1
					chunkMinedBlocks = chunkMinedBlocks + 1
					minerBlocks = minerBlocks + 1
					if blockHashes[blkNum] != blockHash:
						numForkedBlocks = numForkedBlocks + 1
						print(blkNum, end=" ")
			if minerId in minedBlocks.keys():
				# print(i, minerBlocks, minedBlocks[minerId])
				mainChainRatio[i] = minedBlocks[minerId]/minerBlocks
			# if i <= 2:
			# 	print("(",i,minerBlocks,")", end=" ")
		else:
			print("Error", fileName, "file not found")
		if minerBlocks != 0:
			print("\n",numForkedBlocks, minerBlocks, 1-numForkedBlocks/minerBlocks,"\n\n")
	# print()
	# print(delay, totalMinedBlocks)
	return mainChainRatio
	
def forkRateDelay(strategy="", numChunk=1):
	global totalMinedBlocks, chunkMinedBlocks

	dirPath = '/home/sourav/EVD-Segate1/EVD500M-'	
	delays = [1, 4, 2]
	gasUsage = 500
	chunkResults = {}
	outputFilePath = os.environ["HOME"]+"/EVD/writeup-EVD/data/evd-minefrac-delay"+str(strategy)+".csv"

	outputFile = open(outputFilePath,"w+")
	outputFile.write("delay,gasUsage,totalMainChain,totalMined,forkRate,cfiFork,frac1,cfi1,frac2,cfi2,frac3,cfi3\n")

	totalBlocks = 950
	for delay in delays:

		if delay == 2 and strategy=='':
			dirPath = '/home/sourav/EVD-Segate1/EVD-Short/EVD500M-'
			numChunk = 2
			totalBlocks = 150

		totalMinedBlocks = 0
		chunkResults[delay] = {}
		chunkResults[delay][0] = []
		chunkResults[delay][1] = []
		chunkResults[delay][2] = []

		forkRates = []
		meanFrac = {}
		cfiFrac = {}

		inputFilePath =  dirPath+str(delay)+"x"+str(strategy)+"/"
		
		startBlk = 50
		endBlk = startBlk+totalBlocks/numChunk
		for j in range(0,numChunk):
			mainChainRatio = computeForkRate(inputFilePath, outputFile, startBlk, endBlk, strategy, delay)
			# print(strategy, delay, mainChainRatio,"\n")
			startBlk = endBlk+1
			chunkSize = totalBlocks/numChunk
			endBlk = startBlk+chunkSize

			print(delay, chunkMinedBlocks)
			forkRates.append(100*chunkSize/chunkMinedBlocks)
			for k in range(0,3):
				chunkResults[delay][k].append(100*mainChainRatio[k])
		


		meanForkRate = np.mean(forkRates)
		stdDevForkRate = np.std(forkRates)
		cfiForkRate = 1.984*stdDevForkRate/math.sqrt(10)

		for j in range(0,3):
			meanFrac[j] = np.mean(chunkResults[delay][j])
			stdDev = np.std(chunkResults[delay][j])
			cfiFrac[j] = 2.262*stdDev/math.sqrt(10)

		outputFile.write(str(delay*1.0)+","+str(gasUsage)+","+str(totalBlocks)+","+str(totalMinedBlocks)+","+str(meanForkRate)+","+str(cfiForkRate))
		for j in range(0,3):
			outputFile.write(","+str(meanFrac[j])+","+str(cfiFrac[j]))
		outputFile.write("\n")
		# avgLateBlock = np.mean(blockFractList)
		# stdDev = np.std(blockFractList)
		# confidenceInterVal = 1.984*stdDev/math.sqrt(10)

		# print(avgLateBlock, stdDev, confidenceInterVal)
		# outputFile.write(str(confidenceInterVal)+"\n")
		# print("\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n")	

def forkRateGas(strategy="", numChunk=1, evd=True):
	global totalMinedBlocks, chunkMinedBlocks
	delay = 1
	gasUsages = [12,120,240]
	chunkResults = {}

	dirPath = ""
	outputFilePath = ""
	if evd:
		dirPath = '/home/sourav/EVD-Segate1/EVD'	
		outputFilePath = os.environ["HOME"]+"/EVD/writeup-EVD/data/evd-minefrac"+str(strategy)+".csv"
	else:	
		dirPath = '/home/sourav/EVD-Segate1/ETH'	
		outputFilePath = os.environ["HOME"]+"/EVD/writeup-EVD/data/eth-minefrac"+str(strategy)+".csv"
	outputFile = open(outputFilePath,"w+")
	outputFile.write("delay,gasUsage,totalMainChain,totalMined,forkRate,cfiFork,frac1,cfi1,frac2,cfi2,frac3,cfi3\n")

	totalBlocks = 950
	for gasUsage in gasUsages:
		totalMinedBlocks = 0
		chunkResults[gasUsage] = {}
		chunkResults[gasUsage][0] = []
		chunkResults[gasUsage][1] = []
		chunkResults[gasUsage][2] = []

		forkRates = []
		meanFrac = {}
		cfiFrac = {}

		inputFilePath =  dirPath+str(gasUsage)+"M"+str(strategy)+"/"
		startBlk = 50
		chunkSize = totalBlocks/numChunk
		endBlk = startBlk+chunkSize
		for j in range(0,numChunk):
			mainChainRatio = computeForkRate(inputFilePath, outputFile, startBlk, endBlk, strategy, delay, evd)
			# print(strategy, delay, mainChainRatio,"\n")
			startBlk = endBlk+1
			endBlk = startBlk+totalBlocks/numChunk

			forkRates.append(100*chunkSize/chunkMinedBlocks)
			for k in range(0,3):
				chunkResults[gasUsage][k].append(100*mainChainRatio[k])
		
		meanForkRate = np.mean(forkRates)
		stdDevForkRate = np.std(forkRates)
		cfiForkRate = 2.262*stdDevForkRate/math.sqrt(10)

		for j in range(0,3):
			meanFrac[j] = np.mean(chunkResults[gasUsage][j])
			stdDev = np.std(chunkResults[gasUsage][j])
			cfiFrac[j] = 2.262*stdDev/math.sqrt(10)

		outputFile.write(str(delay)+","+str(gasUsage)+","+str(totalBlocks)+","+str(totalMinedBlocks)+","+str(meanForkRate)+","+str(cfiForkRate))
		for j in range(0,3):
			outputFile.write(","+str(meanFrac[j])+","+str(cfiFrac[j]))
		outputFile.write("\n")
		print(gasUsage, meanFrac, cfiFrac)


# forkRateDelay("-skip")
totalMinedBlocks = 0
chunkMinedBlocks = 0

if len(sys.argv) <3:
	print(" [eth,evd,delay], numChunk")
	exit()
numChunk = int(sys.argv[2])
if sys.argv[1] == 'eth':
	forkRateGas("-skip", numChunk, False)
	print("\n\n\n\n\n")
	forkRateGas("", numChunk, False)
elif sys.argv[1] == 'delay':
	forkRateDelay("-skip", numChunk)
	print("\n\n\n\n\n")
	forkRateDelay("", numChunk)
elif sys.argv[1] == 'evd':
	forkRateGas("-skip", numChunk, True)
	print("\n\n\n\n\n")
	forkRateGas("", numChunk, True)
else:
	print("eth,evd,delay")