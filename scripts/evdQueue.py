'''
This python file analyzes information collected regarding
queues during EVD experiments.

EVD-NS-D:
EVD800_1xDelay  EVD800_2xDelay  EVD800_4xDelay

EVD-NS-ND:
EVD-400-NoSkip-1x-Het  EVD-40-NoSkip-1x-Het  EVD-800-NoSkip-1x-Het

EVD-S-D:
EVD120_1xDelay_With_skip  EVD12_1xDelay_With_skip  EVD240_1xDelay_With_skip

'''
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import os 
import sys
from collections import defaultdict

filePath = '/home/nitin14/EVD-Segate/'

evdDir = [
	'EVD-NS-D',
	'EVD-NS-ND',
	'EVD-S-D'
]

def maximum(a, b, c): 
  
    if (a >= b) and (a >= b): 
        largest = a 
  
    elif (b >= a) and (b >= a): 
        largest = b 
    else: 
        largest = c 
          
    return largest


def calcQueueSizeFreq(inputFilePath, outputFile, startBlk, endBlk, exIndex, delay):
	
	# 1 0x5d977ab758447499bbf0fe1d7dc08bed02faba8e127343c9142e5752c2d465b7 0 1
	minDataSize = 1000
	#print(inputFilePath)
	pendingQueueAtMiner = {} # dictionary of the form index:{}
	pendingQueueGlobal = {}

	for j in range(1,49):

		pendingQueueAtMiner[j] = {}
		
		fileName = inputFilePath+'Ql/'+str(j)+'.dat'
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()
			#print("*************inside")
			# if j==0:
			# 	minDataSize = len(data)

			shouldContinue = 0
			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				if int(info[2]) > 50:

					shouldContinue = 1
					break
			if shouldContinue == 1:
				print("node1: "+str(j))
				if len(data) < minDataSize:
				
					print("node2: "+str(j))
				continue

			if len(data) < minDataSize:
				# print("Skipping information of node",str(j)," contains only ", str(len(data)), "data points")
				print("node: "+str(j))
				continue
			# print("actual node value : "+str(j))	
			if j == 0:
				continue

			
			blkNum = 0
			prevBlkNum =0
			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				blkNum = int(info[0])
				if blkNum < startBlk:
					prevBlkNum = blkNum
					continue
				elif blkNum > endBlk:
					break
				else:
					pqLen = int(info[2])
					for diff in range(0,blkNum-prevBlkNum):
					# if pqLen == 6:
					# 	print("***********")
						if pqLen in pendingQueueAtMiner[j]:
							pendingQueueAtMiner[j][pqLen] = pendingQueueAtMiner[j][pqLen] + 1
							pendingQueueGlobal[pqLen] =  pendingQueueGlobal[pqLen] + 1
						else:
							pendingQueueAtMiner[j][pqLen] = 1
							if pqLen not in pendingQueueGlobal:
								pendingQueueGlobal[pqLen] = 1
						pqLen=pqLen-1
		else:
			print("Error", fileName, "file not found")
	# print()
	
	prunedQueueGlobal = {}
	for i in sorted(pendingQueueGlobal):
		#print(i,":", pendingQueueGlobal[i],)
		prunedQueueGlobal[i] = pendingQueueGlobal[i]
		if i > 50:
			break
	#print(len(pendingQueueGlobal))

	# prunedKeys = list(prunedQueueGlobal.keys())
	# if len(pendingQueueGlobal) > 25:
	# 	prunedLen = len(prunedKeys)
	# 	j = prunedLen-1
	# 	while j >= 0:
	# 		key1 = int(prunedKeys[j])
	# 		key2 = int(prunedKeys[j-1])
	# 		if key1-key2 > 1:
	# 			del prunedQueueGlobal[key1]
	# 			break
	# 		elif key1 <= 10:
	# 			break
	# 		else:
	# 			del prunedQueueGlobal[key1]
	# 		j=j-1

	#print(prunedQueueGlobal)
	# print()
	return prunedQueueGlobal

def calcQueueEVDSkip():
	dirPath = '/home/nitin14/EVD-Scripts/statsData/EVD'

	gasList = [12,120,240]
	fileNames =[
		'EVD12_1xDelay_With_skip/',
		'EVD120_1xDelay_With_skip/',
		'EVD240_1xDelay_With_skip/',
	]

	lenFileNames = len(gasList)
	outputFilePath = '/home/nitin14/EVD-Scripts/queueEvdSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("queueLen,fracBlock12,cfi1,fracBlock120,cfi2,fracBlock240,cfi3\n")
	queueStats = []
	for i in range(0,lenFileNames):
		globalQueueFract = defaultdict(list)
		inputFilePath =  dirPath+str(gasList[i])+"M-skip/"
		startBlk = 50
		endBlk = startBlk+95
		maxTillNow = 0
		for k in range(0,10):
			queueStat = calcQueueSizeFreq(inputFilePath, outputFile, startBlk, endBlk, 1, 1)
			
			sumCfi = sum(queueStat.values())
			maxQueueLen = max(queueStat, key=int)
			# print(maxQueueLen)
			# if maxQueueLen == 6:
			#print(maxQueueLen)	
			#print(queueStat)
			if maxTillNow < maxQueueLen:
				maxTillNow = maxQueueLen
			for j in range(0, maxQueueLen+1):
				if j in queueStat:
					globalQueueFract[j].append(queueStat[j]/sumCfi)

			#print(globalQueueFract[6])		
			startBlk = endBlk+1
			endBlk = startBlk+95
		#for j in range(0, maxTillNow+1):	
		#	print(globalQueueFract[j])	
		#print(maxTillNow)	
		for j in range(0, maxTillNow+1):
			if len(globalQueueFract[j]) != 0:
				avgLateBlock = np.mean(globalQueueFract[j])
				stdDev = np.std(globalQueueFract[j])
				confidenceInterVal = 1.984*stdDev/math.sqrt(10)
				cfIntervalList[i].append(confidenceInterVal)
			else:
				cfIntervalList[i].append(0.0)

		print(cfIntervalList[i])

		queueStat = calcQueueSizeFreq(inputFilePath, outputFile, 50, 1000, 1, 1)
		queueStats.append(queueStat)

	len1 = max(queueStats[0], key=int)
	len2 = max(queueStats[1], key=int)
	len3 = max(queueStats[2], key=int)

	sum1 = sum(queueStats[0].values())
	sum2 = sum(queueStats[1].values())
	sum3 = sum(queueStats[2].values())
	
	maxQueueLen = maximum(len1, len2, len3)

	for i in range(0, maxQueueLen):
		frac1 = 0
		frac2 = 0
		frac3 = 0
		cfi1 = 0.0
		cfi2 = 0.0
		cfi3 = 0.0

		if i in queueStats[0]:
			frac1 = queueStats[0][i]/sum1
			cfi1 = cfIntervalList[0][i]
		if i in queueStats[1]:
			frac2 = queueStats[1][i]/sum2
			cfi2 = cfIntervalList[1][i]
		if i in queueStats[2]:
			frac3 = queueStats[2][i]/sum3
			cfi3 = cfIntervalList[2][i]

		outputFile.write(str(i)+","+str(frac1)+","+str(cfi1)+","+str(frac2)+","+str(cfi2)+","+str(frac3)+","+str(cfi3)+"\n")


#globalQueueFract = []
#globalQueueFractCfi = []
#globalQueueFract = defaultdict(list)
cfIntervalList = defaultdict(list)
def calcQueueEVDNoSkip():
	dirPath = '/home/nitin14/EVD-Scripts/statsData/EVD'
	gasList = [12,120,240]
	fileNames =[
		'EVD-40-NoSkip-1x-Het/',
		'EVD-400-NoSkip-1x-Het/',
		'EVD-800-NoSkip-1x-Het/'
	]

	lenFileNames = len(gasList)
	outputFilePath = '/home/nitin14/EVD-Scripts/queueEvdNoSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("queueLen,fracBlock40,cfi1,fracBlock400,cfi2,fracBlock800,cfi2\n")
	
	queueStats = []
	for i in range(0,lenFileNames):
		globalQueueFract = defaultdict(list)
		inputFilePath =  dirPath+str(gasList[i])+"M/"
		startBlk = 50
		endBlk = startBlk+95
		maxTillNow = 0
		for k in range(0,10):
			queueStat = calcQueueSizeFreq(inputFilePath, outputFile, startBlk, endBlk, 0, 1)
			
			sumCfi = sum(queueStat.values())
			maxQueueLen = max(queueStat, key=int)
			# print(maxQueueLen)
			# if maxQueueLen == 6:
			# 	print(queueStat)
			if maxTillNow < maxQueueLen:
				maxTillNow = maxQueueLen
			for j in range(0, maxQueueLen+1):
				if j in queueStat:
					globalQueueFract[j].append(queueStat[j]/sumCfi)

			#print(globalQueueFract[6])		
			startBlk = endBlk+1
			endBlk = startBlk+95

		for j in range(0, maxTillNow+1):
			if len(globalQueueFract[j]) != 0:
				avgLateBlock = np.mean(globalQueueFract[j])
				stdDev = np.std(globalQueueFract[j])
				confidenceInterVal = 1.984*stdDev/math.sqrt(10)
				cfIntervalList[i].append(confidenceInterVal)
			else:
				cfIntervalList[i].append(0.0)

		print(cfIntervalList[i])			

		queueStat = calcQueueSizeFreq(inputFilePath, outputFile, 50, 1000, 0, 1)
		queueStats.append(queueStat)

	len1 = max(queueStats[0], key=int)
	len2 = max(queueStats[1], key=int)
	len3 = max(queueStats[2], key=int)

	sum1 = sum(queueStats[0].values())
	sum2 = sum(queueStats[1].values())
	sum3 = sum(queueStats[2].values())

	maxQueueLen = maximum(len1, len2, len3)
	# maxQueueLen = len1
	for i in range(0, maxQueueLen):
		frac1 = 0
		frac2 = 0
		frac3 = 0
		cfi1 = 0.0
		cfi2 = 0.0
		cfi3 = 0.0

		if i in queueStats[0]:
			frac1 = queueStats[0][i]/sum1
			cfi1 = cfIntervalList[0][i]
		if i in queueStats[1]:
			frac2 = queueStats[1][i]/sum2
			cfi2 = cfIntervalList[1][i]
		if i in queueStats[2]:
			frac3 = queueStats[2][i]/sum3
			cfi3 = cfIntervalList[2][i]

		outputFile.write(str(i)+","+str(frac1)+","+str(cfi1)+","+str(frac2)+","+str(cfi2)+","+str(frac3)+","+str(cfi3)+"\n")

	    
def calcQueueEVDDelay():
	# dirPath = '/home/nitin14/EVD-Scripts/statsData/EVD500M-'
	dirPath = '/home/soruav/EVD-Segate1/EVD500M-'
	delays = [1, 2, 4]

	lenFileNames = len(delays)
	outputFilePath = '/home/EVD-Expt/data/queueEvdDelay.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("queueLen,fracBlock1,cfi1,fracBlock2,cfi2,fracBlock4,cfi4\n")
	
	queueStats = []
	for i in range(0,lenFileNames):
		globalQueueFract = defaultdict(list)
		inputFilePath =  dirPath+str(delays[i])+"x-skip/"
		# startBlk = 50
		# endBlk = startBlk+95
		# maxTillNow = 0
		#print(str(i))
		# for k in range(0,10):
		# 	queueStat = calcQueueSizeFreq(inputFilePath, outputFile, startBlk, endBlk, 0, delays[i])
		# 	#print(queueStat)
		# 	sumCfi = sum(queueStat.values())
		# 	maxQueueLen = max(queueStat, key=int)
		# 	# print(maxQueueLen)
		# 	# if maxQueueLen == 6:
			
		# 	if maxTillNow < maxQueueLen:
		# 		maxTillNow = maxQueueLen
		# 	for j in range(0, maxQueueLen+1):
		# 		if j in queueStat:
		# 			globalQueueFract[j].append(queueStat[j]/sumCfi)

		# 	#print(globalQueueFract[6])		
		# 	startBlk = endBlk+1
		# 	endBlk = startBlk+95

		# for j in range(0, maxTillNow+1):
		# 	if len(globalQueueFract[j]) != 0:
		# 		avgLateBlock = np.mean(globalQueueFract[j])
		# 		stdDev = np.std(globalQueueFract[j])
		# 		confidenceInterVal = 1.984*stdDev/math.sqrt(10)
		# 		cfIntervalList[i].append(confidenceInterVal)
		# 	else:
		# 		cfIntervalList[i].append(0.0)

		# print(cfIntervalList[i])

		queueStat = calcQueueSizeFreq(inputFilePath, outputFile, 50, 1000, 0, delays[i])
		queueStats.append(queueStat)
		print("*****************"+str(delays[i]))

	len1 = max(queueStats[0], key=int)
	len2 = max(queueStats[1], key=int)
	len3 = max(queueStats[2], key=int)

	sum1 = sum(queueStats[0].values())
	sum2 = sum(queueStats[1].values())
	sum3 = sum(queueStats[2].values())
	
	maxQueueLen = maximum(len1, len2, len3)

	cQueueFrac = {}


	frac1 = 0
	frac2 = 0
	frac3 = 0
	for i in range(0, maxQueueLen):
		cfi1 = 0.0
		cfi2 = 0.0
		cfi3 = 0.0

		if i in queueStats[0]:
			frac1 = frac1 + queueStats[0][i]/sum1
			#cfi1 = cfIntervalList[0][i]
		if i in queueStats[1]:
			frac2 = frac2 + queueStats[1][i]/sum2
			#cfi2 = cfIntervalList[1][i]
		if i in queueStats[2]:
			frac3 = frac3 + queueStats[2][i]/sum3
			#cfi3 = cfIntervalList[2][i]

		outputFile.write(str(i)+","+str(frac1)+","+str(cfi1)+","+str(frac2)+","+str(cfi2)+","+str(frac3)+","+str(cfi3)+"\n")


#calcQueueEVDSkip()
#calcQueueEVDNoSkip()
calcQueueEVDDelay()