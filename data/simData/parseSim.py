 	 		'''
This file extracts useful information from the results
of discrete event simulation

sim-res-mine25.txt
sim-res-rest25.txt

-----------------------------------
Adversarial Strategy: mine
Global Inter arrival: 10.0
K:25	 maximum K+N: unbounded
adversary fraction: 0.3333333333333333
Block Processing Time: 5.0
-----------------------------------
Iteration,NumBlocks,NumLateBlocks,fracLateBlocks,SimTime
0,1000000,726,0.000726,7.478754

'''

import sys
import time
import math 
import numpy as np
import os

from decimal import *
getcontext().prec = 400


def analyzeResults(strategy, queueLen):
	avgLateBlock = 0.0
	confidenceInterVal = 0.0
	numData = 100
	lateBlocks = np.zeros([1,numData])
	
	fileName = os.environ["HOME"]+"/EVD-Expt/data/simData/sim-res-"+strategy+str(queueLen)+".txt"
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		i = 0
		for dataItem in data:
			# Skipping first few additional Information
			if dataItem[0] != '0':
				continue 
			info = dataItem.rstrip().split(',')
			lateBlocks[i] = float(info[3])
			i = i+1

		avgLateBlock = np.mean(lateBlocks)
		stdDev = np.std(lateBlocks)
		confidenceInterVal = 1.984*stdDev/math.sqrt(numData)
	else:
		print(fileName," file not found!!")

	return(avgLateBlock, confidenceInterVal)

strategies = ['mine', 'reset']
results = {} # 'mine':<>, 'reset':<>
for strategy in strategies:
	stratRes = {}
	for k in range(25,75,10):
		avg, cfi = analyzeResults(strategy,k)
		print(avg, cfi)
		stratRes[k] = {'avg':avg, 'cfi':cfi}
	results[strategy] = stratRes

outFilePath = os.environ["HOME"]+"/EVD-Expt/data/simData/sim-res.csv"
outFile = open(outFilePath, "a+")
outFile.write("queueLen,mineAvgLate,mineCfi,resetAvgLate,resetAvgCfi\n")


for k in range(25,75,10):
	outFile.write(str(k))
	for strategy in strategies:
		avgLate = results[strategy][k]['avg']
		avgCfi = results[strategy][k]['cfi']
		outFile.write(","+str(avgLate)+","+str(avgCfi))
	outFile.write("\n")



