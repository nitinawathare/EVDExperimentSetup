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


def analyzeResults(strategy):

	global probResults, cfiResults
	numData = 10

	for k in range(15,70,10):
		probResults[k] = {}
		cfiResults[k] = {}

		for consTh in range(15,70,10):
			fileName = os.environ["HOME"]+"/EVD-Expt/des/dsDataCopy/k"+str(k)+"/sim-res-"+strategy+str(consTh)+".txt"
			if os.path.exists(fileName):
				file = open(fileName, "r")
				data = file.readlines()
				dataFound = True
				i = 0
				successProbs = np.zeros([1,numData])
				for dataItem in data:
					if not dataItem[0].isdigit():
						continue 
					info = dataItem.rstrip().split(',')
					successProbs[0][i] = float(info[7])
					i = i+1

				avgSucussProb = np.mean(successProbs[0])
				stdDev = np.std(successProbs[0])
				confidenceInterVal = 2.262*stdDev/math.sqrt(numData)
				print(k, consTh, avgSucussProb, stdDev, confidenceInterVal)
				probResults[k][consTh] = avgSucussProb
				cfiResults[k][consTh] = confidenceInterVal
			else:
				print(fileName," file not found!!")


strategies = ['ds']
probResults = {} 
cfiResults = {}

for strategy in strategies:
	analyzeResults(strategy)

outFilePath = os.environ["HOME"]+"/EVD-Expt/des/dsDataCopy/sim-res.csv"
outFile = open(outFilePath, "a+")

outFile.write("constTh")
for k in range(15,75,10):
	outFile.write(",k"+str(k)+",cfi"+str(k))
outFile.write("\n")

for constTh in range(15,70,10):
	outFile.write(str(constTh))
	for k in range(15,70,10):
		if k == 55 and constTh == 65:
			outFile.write(",,")
		else:
			outFile.write(","+str(probResults[k][constTh])+","+str(cfiResults[k][constTh]))
	outFile.write("\n")
