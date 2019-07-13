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

import time
import numpy as np
import matplotlib.pyplot as plt
import os 
import sys


filePath = '/home/sourav/EVD-Segate/'

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
	minDataSize = 500
	print(inputFilePath)
	pendingQueueAtMiner = {} # dictionary of the form index:{}
	pendingQueueGlobal = {}

	for j in range(0,49):

		pendingQueueAtMiner[j] = {}
		
		fileName = inputFilePath+'Ql/'+str(j)+'.dat'
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			# if j==0:
			# 	minDataSize = len(data)

			if len(data) < minDataSize:
				# print("Skipping information of node",str(j)," contains only ", str(len(data)), "data points")
				continue

			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				blkNum = int(info[0])
				if blkNum < startBlk:
					continue
				elif blkNum > endBlk:
					break
				else:
					pqLen = int(info[2])
					if pqLen in pendingQueueAtMiner[j]:
						pendingQueueAtMiner[j][pqLen] = pendingQueueAtMiner[j][pqLen] + 1
						pendingQueueGlobal[pqLen] =  pendingQueueGlobal[pqLen] + 1
					else:
						pendingQueueAtMiner[j][pqLen] = 1
						if pqLen not in pendingQueueGlobal:
							pendingQueueGlobal[pqLen] = 1
		else:
			print("Error", fileName, "file not found")
	# print()
	
	prunedQueueGlobal = {}
	for i in sorted(pendingQueueGlobal):
		# print(i,":", pendingQueueGlobal[i],)
		prunedQueueGlobal[i] = pendingQueueGlobal[i]
		if i > 25:
			break
	# print(len(pendingQueueGlobal))

	prunedKeys = list(prunedQueueGlobal.keys())
	if len(pendingQueueGlobal) > 25:
		prunedLen = len(prunedKeys)
		j = prunedLen-1
		while j >= 0:
			key1 = int(prunedKeys[j])
			key2 = int(prunedKeys[j-1])
			if key1-key2 > 1:
				del prunedQueueGlobal[key1]
				break
			elif key1 <= 10:
				break
			else:
				del prunedQueueGlobal[key1]
			j=j-1

	# print(prunedQueueGlobal)
	# print()
	return prunedQueueGlobal

def calcQueueEVDSkip():
	dirPath = '/home/sourav/EVD-Segate/EVD-S-D/'

	gasList = [12, 120, 240]
	fileNames =[
		'EVD12_1xDelay_With_skip/',
		'EVD120_1xDelay_With_skip/',
		'EVD240_1xDelay_With_skip/',
	]

	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/queueEvdSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("queueLen,fracBlock12,fracBlock120,fracBlock240\n")
	queueStats = []
	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
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
		if i in queueStats[0]:
			frac1 = queueStats[0][i]/sum1

		if i in queueStats[1]:
			frac2 = queueStats[1][i]/sum2
		
		if i in queueStats[2]:
			frac3 = queueStats[2][i]/sum3
				
		outputFile.write(str(i)+","+str(frac1)+","+str(frac2)+","+str(frac3)+"\n")


def calcQueueEVDNoSkip():
	dirPath = '/home/sourav/EVD-Segate/EVD-NS-ND/'
	gasList = [40, 400, 800]
	fileNames =[
		'EVD-40-NoSkip-1x-Het/',
		'EVD-400-NoSkip-1x-Het/',
		'EVD-800-NoSkip-1x-Het/'
	]

	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/queueEvdNoSkip.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("queueLen,fracBlock40,fracBlock400,fracBlock800\n")
	
	queueStats = []
	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		queueStat = calcQueueSizeFreq(inputFilePath, outputFile, 50, 1000, 0, 1)
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
		if i in queueStats[0]:
			frac1 = queueStats[0][i]/sum1

		if i in queueStats[1]:
			frac2 = queueStats[1][i]/sum2
		
		if i in queueStats[2]:
			frac3 = queueStats[2][i]/sum3
				
		outputFile.write(str(i)+","+str(frac1)+","+str(frac2)+","+str(frac3)+"\n")

	    
def calcQueueEVDDelay():
	dirPath = '/home/sourav/EVD-Segate/EVD-NS-D/'
	delays = [1, 2, 4]
	fileNames =[
		'EVD800_1xDelay/',
		'EVD800_2xDelay/',
		'EVD800_4xDelay/'
	]

	lenFileNames = len(fileNames)
	outputFilePath = '/home/sourav/EVD-Expt/data/queueEvdDelay.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("queueLen,fracBlock1,fracBlock2,fracBlock4\n")
	
	queueStats = []
	for i in range(0,lenFileNames):
		inputFilePath =  dirPath+fileNames[i]
		queueStat = calcQueueSizeFreq(inputFilePath, outputFile, 50, 1000, 0, delays[i])
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
		if i in queueStats[0]:
			frac1 = queueStats[0][i]/sum1

		if i in queueStats[1]:
			frac2 = queueStats[1][i]/sum2
		
		if i in queueStats[2]:
			frac3 = queueStats[2][i]/sum3
				
		outputFile.write(str(i)+","+str(frac1)+","+str(frac2)+","+str(frac3)+"\n")



calcQueueEVDSkip()
calcQueueEVDNoSkip()
calcQueueEVDDelay()