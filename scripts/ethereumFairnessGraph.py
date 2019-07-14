''' 
Note : Here you may have to rename the data folder accordingly 

This script calculates the fraction of blocks mined by miner 
in the main chain and expected number of block mined by 
a miner present in the main chain based on his mining power

ETH-NS-D-HET:
ETH-400-NoSkip-1x-Het

ETH-NS-D-HOMO:
ETH-40-NoSkip-1x-Homo

ETH-NS-ND-HET:
ETH-40-NoSkip-1x-Het  ETH-800-NoSkip-1x-Het

ETH-NS-ND-HOMO:
ETH-40-NoSkip-XX-Homo

ETH-S-ND:
ETH-120-Skip-1x  ETH-12-Skip-1x  ETH-240-Skip-1x

EVD-NS-D:
EVD800_1xDelay  EVD800_2xDelay  EVD800_4xDelay

EVD-NS-ND:
EVD-400-NoSkip-1x-Het  EVD-40-NoSkip-1x-Het  EVD-800-NoSkip-1x-Het

EVD-S-D:
EVD120_1xDelay_With_skip  EVD12_1xDelay_With_skip  EVD240_1xDelay_With_skip

'''

import time
import numpy as np
import matplotlib.pyplot as plt
import os 
import sys


filePath = '/home/sourav/EVD-Segate/'

ethDir = [
	'ETH-NS-D-HET',
	'ETH-NS-D-HOMO',
	'ETH-NS-ND-HET',
	'ETH-NS-ND-HOMO',
	'ETH-S-ND'
]

evdDir = [
	'EVD-NS-D',
	'EVD-NS-ND',
	'EVD-S-D'
]

def computeFairness(inputFilePath, outputFile, startBlk, endBlk, exIndex, evd, delay):
	
	# 0xdb719d2e7cc1390e46f141a2e4978e9f49f16d63242c5d66f99aa33fef2e5300 15 282 400000000 396576869 0xbd611E337D54dfdbe9A052Fe689a7486cB59156c 664.650ms

	# Extracting address of the first node
	fileName = inputFilePath+'Mi/0.dat'
	firstMiner = ""
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()
		if evd:
			firstMiner = data[0].rstrip().split(' ')[8]
		else:
			firstMiner = data[0].split(' ')[5]

	# Blocks in the main chain of the first miner.
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

	# Compute the effective active hash power at every block.
	for j in range(1,49):
		fileName = inputFilePath+'Mc/'+str(j)+'.dat'
		if os.path.exists(fileName):
			file =  open(fileName, "r")
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
					if blkHash == blockHashes[blkNum]:
						hashPowerAtBlock[blkNum] = hashPowerAtBlock[blkNum] + hashPowers[j]
		else:
			print("Error", fileName, "file not found")
			break

	exptBlkCount = 0.0
	for k in range(startBlk, endBlk):
		exptBlkCount = exptBlkCount + hashPowers[0]/hashPowerAtBlock[k]

		# if k%50 == 0:
		# 	print(hashPowerAtBlock[k], hashPowers[0]/hashPowerAtBlock[k])

	# 14,0x79068e34c77770f599afe5bf18f70326e7c4744b712a28d9ccba282eee91c65c,0xbd611E337D54dfdbe9A052Fe689a7486cB59156c,283,400000000,398949296
	# Compute the number of blocks mined by a miner in 
	miningFrac = {}
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
				if miningFrac.get(miner):
					miningFrac[miner] = miningFrac[miner] + 1
				else:
					miningFrac[miner] = 1

	if not evd:
		exTimes = computeEthExecutionTime(inputFilePath, outputFile, startBlk, endBlk, exIndex)
	else:
		exTimes = computeEVDExecutionTime(inputFilePath, outputFile, startBlk, endBlk, exIndex)

	trueMiningPower = exptBlkCount/totalBlkCount
	exptBlkCount = (exptBlkCount*hashPowers[0])/trueMiningPower
	blocksMined = (miningFrac[firstMiner]/totalBlkCount)*hashPowers[0]/trueMiningPower



	print(inputFilePath)	
	# print(exptBlkCount, exptBlkCount/totalBlkCount, miningFrac[firstMiner], miningFrac[firstMiner]/totalBlkCount, totalBlkCount)
	print(exptBlkCount, exptBlkCount/totalBlkCount, miningFrac[firstMiner], blocksMined, totalBlkCount)
	print(exTimes)
	print()

	expFraction = exptBlkCount/totalBlkCount
	actFraction = (miningFrac[firstMiner]/totalBlkCount)*hashPowers[0]/trueMiningPower

	avgAdvExtTime = exTimes[0][0]
	avgAdvProcTime = exTimes[0][1]

	if evd:
		avgHonestExTime = exTimes[2]
		avgHonestProcTime = exTimes[3]
		avgAdvExtTime = exTimes[0][0]
		avgAdvProcTime = exTimes[0][1]
		
		avgHonestPrevTime = exTimes[4]
		avgAdvPrevTime = exTimes[1]

		if exIndex == 1: # Adversary Skips processing
			outputFile.write(str(totalBlkCount)+","+str(delay)+","+str(avgHonestExTime)+","+str(avgHonestProcTime)+","+str(avgHonestPrevTime)+","+str(avgAdvExtTime)+","+str(avgAdvProcTime)+","+str(avgAdvPrevTime)+","+str(expFraction)+","+str( actFraction)+"\n")
		
		elif exIndex == 0:
			outputFile.write(str(totalBlkCount)+","+str(delay)+","+str(avgHonestExTime)+","+str(avgHonestProcTime)+","+str(avgHonestPrevTime)+","+str(expFraction)+","+str( actFraction)+"\n")
	else:
		avgHonestExTime = exTimes[1]
		avgHonestProcTime = exTimes[2]
		if exIndex == 1:
			outputFile.write(str(totalBlkCount)+","+str(delay)+","+str(avgHonestExTime)+","+str(avgHonestProcTime)+","+str(avgAdvExtTime)+","+str(avgAdvProcTime)+","+str(expFraction)+","+str( actFraction)+"\n")
		elif exIndex == 0:
			outputFile.write(str(totalBlkCount)+","+str(delay)+","+str(avgHonestExTime)+","+str(avgHonestProcTime)+","+str(expFraction)+","+str( actFraction)+"\n")
	
def computeEthExecutionTime(inputFilePath, outputFile, startBlk, endBlk, exIndex):
	# 0x8414b5ad8f95e31473f5ab3372729317a07567edd2d9501ad8908105dda110bb 13 0 400000000 0 0x6F75AeB2465dAac2B630667efF18481BE2dEfabd false 0.21846 1.32698
	# Compute the average Execution time:
	avgExTime = {}
	
	globalBlks = 0.0
	globalExTime = 0.0
	globalProcTime = 0.0

	for j in range(0,49):
		fileName = inputFilePath+'Ex/'+str(j)+'.txt'
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			totalExTime = 0.0
			totalProcTime =  0.0
			totalBlks = 0
			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				blkNum = int(info[1])
				if blkNum < startBlk:
					continue
				elif blkNum > endBlk:
					continue
				else:

					if j > exIndex:
						globalBlks = globalBlks + 1
						globalExTime = globalExTime + float(info[7])
						globalProcTime = globalProcTime + float(info[8])

					totalExTime = totalExTime + float(info[7])
					totalProcTime = totalProcTime + float(info[8])
					totalBlks = totalBlks + 1
			if totalBlks > 0:
				avgExTime[j] = [totalExTime/totalBlks, totalProcTime/totalBlks]
				# print(j, totalExTime/totalBlks, totalProcTime/totalBlks, totalBlks)
			else:
				avgExTime[j] = [0.0, 0.0]
				# print(j, 0.0, 0.0, totalBlks)

	# print(globalExTime/globalBlks)
	# print(globalProcTime/globalBlks)
	# print()
	return(avgExTime[0], globalExTime/globalBlks, globalProcTime/globalBlks)
	
def computeEVDExecutionTime(inputFilePath, outputFile, startBlk, endBlk, exIndex):

	avgExTime = {}
	avgPrevExTime = {}

	globalBlks = 0.0
	globalExTime = 0.0
	globalProcTime = 0.0

	# Process Time: 0xd6e44025419860bba1869145de849018322b3e63c7e9d2cc860cdc6238878308 1030 163 3500000 3423000 240000000 239478114 239834716 0xD3FE51D92BB935b20C590c0e1fBc33e407FF4c39 23.93245 36.66314

	# Measure the average immediate execution time
	for j in range(0,49):
		fileName = inputFilePath+'Ex/'+str(j)+'.txt'
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			totalExTime = 0.0
			totalProcTime =  0.0
			totalBlks = 0
			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				blkNum = int(info[3])
				if blkNum < startBlk:
					continue
				elif blkNum > endBlk:
					continue
				else:

					if j > exIndex:
						globalBlks = globalBlks + 1
						globalExTime = globalExTime + float(info[11])
						globalProcTime = globalProcTime + float(info[12])

					totalExTime = totalExTime + float(info[11])
					totalProcTime = totalProcTime + float(info[12])
					totalBlks = totalBlks + 1
			if totalBlks > 0:
				avgExTime[j] = [totalExTime/totalBlks, totalProcTime/totalBlks]
				# print(j, totalExTime/totalBlks, totalProcTime/totalBlks, totalBlks)
			else:
				avgExTime[j] = [0.0, 0.0]
				# print(j, 0.0, 0.0, totalBlks)


	# ProcessPrevious Time: 0xe60bd934ad28b96753b2993d27308aeafec9f26c2a8bab08751486486ea3ce84 1030 163 3500000 3423000 240000000 239586771 239834716 0x35eC34902a43d5060E98891B7090250E9aAcF034 true 49.97372

	globalPrevBlks = 0.0
	globalPrevExTime = 0.0
	globalPrevProcTime = 0.0

	for j in range(0,49):
		fileName = inputFilePath+'PPt/'+str(j)+'.dat'
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			totalPrevExTime = 0.0
			totalPrevProcTime =  0.0
			totalPrevBlks = 0
			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				blkNum = int(info[3])
				if blkNum < startBlk:
					continue
				elif blkNum > endBlk:
					continue
				else:

					if j > exIndex:
						globalPrevBlks = globalPrevBlks + 1
						globalPrevExTime = globalPrevExTime + float(info[12])

					totalPrevExTime = totalPrevExTime + float(info[12])
					totalPrevBlks = totalPrevBlks + 1
			if totalPrevBlks > 0:
				avgPrevExTime[j] = totalPrevExTime/totalPrevBlks
				# print(j, totalExTime/totalBlks, totalProcTime/totalBlks, totalBlks)
			else:
				avgPrevExTime[j] = 0.0
	

	# print(globalExTime/globalBlks, globalProcTime/globalBlks)
	# print(globalPrevExTime/globalPrevBlks)
	# print()
	return(avgExTime[0], avgPrevExTime[0], globalExTime/globalBlks, globalProcTime/globalBlks, globalPrevExTime/globalPrevBlks)


def computeEthSkip():
	dirPath = '/home/sourav/EVD-Segate/ETH-S-ND/'
	gasList = [12, 120, 240]
	fileNames =[
		'ETH-12-Skip-1x/',
		'ETH-120-Skip-1x/',
		'ETH-240-Skip-1x/'
	]
	# fileNames =[
	# 	'ETH-240-Skip-1x/'
	# ]

	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/ethSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,avgAdvExtTime,avgAdvProcTime,expFraction,actFraction\n")


	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		computeFairness(inputFilePath, outputFile, 50, 1000, 1, False, 1)

def computeEthNoSkip():
	dirPath = '/home/sourav/EVD-Segate/ETH-NS-ND-HET/'
	dirPath = ''
	gasList = [40, 400, 800]
	fileNames =[
		'/home/sourav/EVD-Segate/ETH-NS-ND-HET/ETH-40-NoSkip-1x-Het/',
		'/home/sourav/EVD-Segate/ETH-NS-D-HET/ETH-400-NoSkip-1x-Het/',
		'/home/sourav/EVD-Segate/ETH-NS-ND-HET/ETH-800-NoSkip-1x-Het/'
	]


	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/ethNoSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,expFraction,actFraction\n")

	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		computeFairness(inputFilePath, outputFile, 50, 1000, 0, False, 1)


def computeEVDSkip():
	dirPath = '/home/sourav/EVD-Segate/EVD-S-D/'

	gasList = [12, 120, 240]
	fileNames =[
		'EVD12_1xDelay_With_skip/',
		'EVD120_1xDelay_With_skip/',
		'EVD240_1xDelay_With_skip/',
	]

	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/evdSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,avgHonestPrevTime,avgAdvExtTime,avgAdvProcTime,avgAdvPrevTime,expFraction,actFraction\n")
	
	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		computeFairness(inputFilePath, outputFile, 50, 1000, 1, True, 1)

def computeEVDNoSkip():
	dirPath = '/home/sourav/EVD-Segate/EVD-NS-ND/'
	gasList = [40, 400, 800]
	fileNames =[
		'EVD-40-NoSkip-1x-Het/',
		'EVD-400-NoSkip-1x-Het/',
		'EVD-800-NoSkip-1x-Het/'
	]

	
	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/evdNoSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,avgHonestPrevTime,expFraction,actFraction\n")
	

	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		computeFairness(inputFilePath, outputFile, 50, 1000, 0, True, 1)
	    
def computeEVDDelay():
	dirPath = '/home/sourav/EVD-Segate/EVD-NS-D/'
	delays = [1, 2, 4]
	fileNames =[
		'EVD800_1xDelay/',
		'EVD800_2xDelay/',
		'EVD800_4xDelay/'
	]

	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/evdDelay.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,avgHonestPrevTime,expFraction,actFraction\n")
	
	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		computeFairness(inputFilePath, outputFile, 50, 1000, 0, True, delays[i])


def readHashPower(fileName):
	hashPowers = []
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			hashPower = float(dataItem.rstrip())
			hashPowers.append(hashPower)
	else:
		print("Error! File ",fileName," not found")

	return hashPowers


hashPowers = readHashPower('/home/sourav/EVD-Expt/hashPower')
hashPowers = [x/sum(hashPowers) for x in hashPowers]


dirPath = '/home/sourav/EVD-Segate/ETH-S-D-15/'
gasList = [12, 120, 240]
fileNames =[
	'ETH-240-Skip-1x/'
]
# fileNames =[
# 	'ETH-240-Skip-1x/'
# ]

lenFileNames = len(fileNames)
outputFilePath = '/home/sourav/EVD-Expt/data/ethSkip1.csv'
outputFile = open(outputFilePath,"w+")
outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,avgAdvExtTime,avgAdvProcTime,expFraction,actFraction\n")


for i in range(0,lenFileNames):
	inputFilePath =  dirPath+fileNames[i]
	computeFairness(inputFilePath, outputFile, 50, 1000, 1, False, 1)


dirPath = '/home/sourav/EVD-Segate/ETH-NS-D-15/'
gasList = [12, 120, 240]
fileNames =[
	'ETH-800-NoSkip-1x-15/'
]
# fileNames =[
# 	'ETH-240-Skip-1x/'
# ]

lenFileNames = len(fileNames)
outputFilePath = '/home/sourav/EVD-Expt/data/ethSkip1.csv'
outputFile = open(outputFilePath,"w+")
outputFile.write("totalBlocks,delay,avgHonestExTime,avgHonestProcTime,avgAdvExtTime,avgAdvProcTime,expFraction,actFraction\n")


for i in range(0,lenFileNames):
	inputFilePath =  dirPath+fileNames[i]
	computeFairness(inputFilePath, outputFile, 50, 1000, 0, False, 1)



# if len(sys.argv) == 1:
# 	print('\n eth-s\n eth-ns\n eth-all\n evd-s\n evd-ns\n evd-all\n')
# elif sys.argv[1] == 'eth-s':
# 	computeEthSkip()
# elif sys.argv[1] == 'eth-ns':
# 	computeEthNoSkip()
# elif sys.argv[1] == 'eth-all':
# 	print("Ethereum No Skip Results")
# 	computeEthNoSkip()
# 	print("Ethereum Skip Results")
# 	computeEthSkip()
# elif sys.argv[1] == 'evd-s':
# 	computeEVDSkip()
# elif sys.argv[1] == 'evd-ns':
# 	computeEVDNoSkip()
# elif sys.argv[1] == 'evd-delay':
# 	computeEVDDelay()
# elif sys.argv[1] == 'evd-all':
# 	computeEVDNoSkip()
# 	computeEVDSkip()
# 	computeEVDDelay()

