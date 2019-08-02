import time
import math
import numpy as np
import matplotlib.pyplot as plt
import os 
import sys
from datetime import datetime
from collections import defaultdict

def proceesRawLog(strategy):
	delay = 1	
	gasList = [12,120,240]
	dirPath = '/home/sourav/EVD-Segate1/ETH'

	lenFileNames = len(gasList)

	fmt = '%Y-%m-%d %H:%M:%S.%f'

	globalQueueFract = defaultdict(list)

	for gas in gasList:
		
		inputFilePath = ""
		if gas == 12:
			inputFilePath = '/home/sourav/EVD-Segate1/EVD'+str(gas)+"M"+strategy+"/"	
		else:
			inputFilePath = dirPath+str(gas)+"M"+strategy+"/"	

		for node in range(0,49):
			
			fileName = inputFilePath+'Log/'+str(node)+'.txt'
			outputFilePath = "/home/sourav/EVD-Expt/ETH-Log/"+str(gas)+strategy+"/Log"+str(node)+'_new.txt'
			print(fileName)

			if os.path.exists(fileName):
				file =  open(fileName, "r")
				data = file.readlines()
				outputFile = open(outputFilePath,"w+")
				previourDataItem = ""
				count = 0
				for dataItem in data:
					info = dataItem.rstrip().split(' ')

					if dataItem.find("Imported new chain segment") != -1:
						tstampCurrent = datetime.strptime("2019-"+info[1][1:-1].split('|')[0]+" "+info[1][1:-1].split('|')[1], fmt)
						numberList = [s for s in info if "number" in s][0]
						number = numberList.split('=')[1]
						blkHashList = [s for s in info if "hash" in s][0]
						blkHash = blkHashList.split('=')[1]
						chunkSizeList = [s for s in info if "blocks" in s][0]
						chunkSize = chunkSizeList.split('=')[1]
						outputFile.write("chain-segment "+str(tstampCurrent)+" "+number+" "+blkHash+" "+chunkSize+"\n")
							# tstampPrev = datetime.strptime(previousTime, fmt)
							# diff = tstampCurrent-tstampPrev
							#if diff.seconds != 0:
							# outputFile.write(str(diff.seconds)+" "+str(info[20].split('=')[1])+"\n")
							#print(str(diff.seconds)+" "+str(info[20]))
							#globalQueueFract[i].append(diff.seconds)
					elif dataItem.find("Successfully sealed new block") != -1:
						tstampCurrent = datetime.strptime("2019-"+info[1][1:-1].split('|')[0]+" "+info[1][1:-1].split('|')[1], fmt)
						numberList = [s for s in info if "number" in s][0]
						number = numberList.split('=')[1]
						blkHashList = [s for s in info if "hash" in s][1]
						blkHash = blkHashList.split('=')[1]
						outputFile.write("sealed-block "+str(tstampCurrent)+" "+number+" "+blkHash+"\n")

					elif dataItem.find("Importing propagated block") != -1:
						numberList = [s for s in info if "number" in s][0]
						number = numberList.split('=')[1]
						blkHashList = [s for s in info if "hash" in s][0]
						blkHash = blkHashList.split('=')[1]
						tstampCurrent = datetime.strptime("2019-"+info[0][6:-1].split('|')[0]+" "+info[0][6:-1].split('|')[1], fmt)
						outputFile.write("forwarded-block "+str(tstampCurrent)+" "+number+" "+blkHash+"\n")

		exit()

def loadTime(startBlk=10, endBlk=1050, strategy=""):
	global sealedResults, rcvdResults

	delay = 1	
	gasList = [12,120,240]
	dirPath = '/home/sourav/EVD-Segate1/ETH'

	lenFileNames = len(gasList)
	fmt = '%Y-%m-%d %H:%M:%S.%f'

	globalQueueFract = defaultdict(list)
	for gas in gasList:
		sealedResults[gas] = {}
		rcvdResults[gas] = {}
		inputFilePath = "/home/sourav/EVD-Expt/ETH-Log/"+str(gas)+strategy+"/"
		for node in range(0,49):
			sealedResults[gas][node] = {}
			rcvdResults[gas][node] = {}

			fileName = inputFilePath+"Log"+str(node)+'_new.txt'
			if os.path.exists(fileName):
				file =  open(fileName, "r")
				data = file.readlines()
				# outputFile = open(outputFilePath,"w+")
				
				for dataItem in data:
					info = dataItem.rstrip().split(' ')
					blkNum = int(info[3])

					if blkNum < startBlk:
						continue
					elif blkNum > endBlk:
						continue
					if len(info[2].split("."))<2:
						info[2] = info[2]+".000000"
					if info[0] == "sealed-block":						
						tstamp = datetime.strptime(info[1]+" "+info[2], fmt)
						blkHash = info[4]
						sealedResults[gas][node][blkHash] = tstamp
					elif info[0] == "chain-segment":
						tstamp = datetime.strptime(info[1]+" "+info[2], fmt)
						blkHash = info[4]
						rcvdResults[gas][node][blkHash] = tstamp
			else:
				print(fileName, "File not found")


def computeAvgDelay(startBlk, endBlk, strategy, lastNode=49):
	global sealedResults, rcvdResults, delayResults
	delay = 1	
	gasList = [12,120,240]

	lenFileNames = len(gasList)
	fmt = '%Y-%m-%d %H:%M:%S.%f'

	globalQueueFract = defaultdict(list)
	results = {}
	for gas in gasList:
		numDelay = 0
		delayValue = []
		delayResults[gas] = {}
		for miner in range(0,lastNode):
			minedBlocks = sealedResults[gas][miner]
			for blockHash in minedBlocks:
				delayResults[blockHash] = []
				minedTime = sealedResults[gas][miner][blockHash]
				for rcvr in range(0,lastNode):
					if blockHash in rcvdResults[gas][rcvr]:
						rcvdTime = rcvdResults[gas][rcvr][blockHash]
						delay = rcvdTime-minedTime
						# if delay.seconds > 20:
						# 	continue
						# delayResults[blockHash].append(delay.microseconds)
						# delayValue.append(delay.microseconds/1000000)

						delayResults[blockHash].append(math.pow(10,6)*delay.seconds +delay.microseconds)
						delayValue.append((math.pow(10,6)*delay.seconds + delay.microseconds)/math.pow(10,6))
						# delayValue = delayValue + delay.seconds
						# if delay.microseconds == 7.0:
						# 	print(delay.microseconds)
						numDelay = numDelay + 1
	
		results[gas] = np.median(delayValue)
	return results






# groupList ={
# 1:[8, 33, 16, 29, 3, 15, 13, 41, 45, 6, 42, 2, 5, 1, 38, 31, 19, 24, 18, 12, 4, 35, 34, 9, 47, 22],
# 2:[7, 25, 0, 20, 37, 11],
# 3:[14, 43, 40, 10, 44, 21],
# 4:[17,30]
# }

# proceesRawLog('-skip')
# proceesRawLog('')

gasList = [12,120,240]
allNoSkipResults = {12:[],120:[],240:[]}
for startBlk in range(50,950,95):
	sealedResults = {}
	rcvdResults = {}
	delayResults = {}
	endBlk = startBlk + 100
	loadTime(startBlk,endBlk)
	noSkipResults = computeAvgDelay(startBlk,endBlk,'',49)
	for gas in gasList:
		allNoSkipResults[gas].append(noSkipResults[gas])

	print("hh")

allSkipResults = {12:[],120:[],240:[]}
for startBlk in range(50,950,95):
	sealedResults = {}
	rcvdResults = {}
	delayResults = {}
	loadTime(startBlk,endBlk,'-skip')
	skipResults = computeAvgDelay(startBlk,endBlk,'-skip',49)
	for gas in gasList:
		allSkipResults[gas].append(skipResults[gas])

	print("ss")


noSkipMean = []
noSkipCfi = []

skipMean = []
skipCfi = []

print("gas,noSkipMean,noSkipCfi,skipMean,skipCfi")
outputFilePath = "/home/sourav/EVD/write-up/data/eth-fork.csv"
outputFile = open(outputFilePath, "w+")
print("gas,noSkipMean,noSkipCfi,skipMean,skipCfi")


for gas in gasList:
	m1 = np.mean(allNoSkipResults[gas])
	s1 = np.std(allNoSkipResults[gas])
	c1 = 2.262*s1/math.sqrt(10)

	# noSkipMean.append(m1)
	# noSkipCfi.append(c1)
	print(str(gas)+","+str(m1)+","+str(c1),end="")

	m1 = np.mean(allSkipResults[gas])
	s1 = np.std(allSkipResults[gas])
	c1 = 2.262*s1/math.sqrt(10)
	print(","+str(m1)+","+str(c1))
	print()

	# skipMean.append(m1)
	# skipCfi.append(c1)


	