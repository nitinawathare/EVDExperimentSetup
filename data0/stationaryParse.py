'''
This file computes the success probability
of an attacker performing an hidden chain
attack. 

State s is the state (s/(M+1), s%(M+1)) where M = k+N

Strategy Reset:
	Number of adv blocks:
		(x-1,x) -> (j,0)	x
		(1,1)	-> (0,0)	{0,1}
		(x, M)	-> (0,0)	M

	Number of honest blocks:
		(0,0)	->	(0,0)	1
		(1,1)	-> 	(0,0)	{0,1}

	Number of Late blocks:
		(k+n-1,k+n) -> (j,0)	n


Strategy Mine:
	Number of adv blocks:
		(x-1,x) -> (j,0)	x + ....
		(1,1)	-> (0,0)	{0,1}
		(x, M)	-> (0,0)	M + ....

	Number of honest blocks:
		(0,0)	->	(0,0)	1
		(1,1)	-> 	(0,0)	{0,1}

	Number of Late blocks:
		(k+n-1,k+n) -> (j,0)	n + ...
	
'''
import sys
import time
import math 
import numpy as np
import os

from decimal import *
getcontext().prec = 400


def toString(numRows):
	for i in range(0,numRows):
		for j in range(0,numRows):
			prob = transProb[i][j]
			if prob > 0:
				print(str(i//maxQueueLen),",",str(i%maxQueueLen), "->", str(j//maxQueueLen),",",str(j%maxQueueLen), ":", prob)

def poissonProb(lambd, k, t):
	nTerm1 = Decimal(math.pow(Decimal(lambd*t), Decimal(k)))
	nTerm2 = Decimal(np.exp(-1*(lambd*t)))
	dTerm1 = Decimal(math.factorial(k))

	return nTerm1*nTerm2/dTerm1

def maxBlockCount(lambd, th, t):
	prob = poissonProb(lambd,0, t)
	numBlocks = 0
	while prob < Decimal(1.0)-th:
		numBlocks = numBlocks + 1
		prob = prob + poissonProb(lambd, numBlocks, t)
	return numBlocks

def expectedBlockCount(lambd, t):
	return lambd*t

def printStates(maxQueueLen):
	for state in range(0, numStates):
		i = state//maxQueueLen
		j = state%maxQueueLen
		print(i,j)
		if j == maxQueueLen - 1:
			print()

def abs(x):
	if x<0:
		return (-1)*x
	else:
		return x

def computeTransProbReset(maxQueueLen, queueLen, lambd, advFrac, t):

	# These seems correct
	transProb[0][0] = Decimal(1.0-advFrac)
	transProb[0][1] = Decimal(advFrac)
	transProb[maxQueueLen+1][0] = Decimal(1.0)
	transProb[1][maxQueueLen+1] = Decimal(1.0-advFrac)
	transProb[1][2] = Decimal(advFrac)

	# These seems correct
	for si in range(2,numStates):	
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy <= queueLen and siy == six+1:
			transProb[si][0] = Decimal(1.0)

		if siy == maxQueueLen-1 and six < siy-1:
			transProb[si][0] = Decimal(advFrac)

	for si in range(2,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen
		sumProb = Decimal(0.0)
		if siy > queueLen and siy == six+1:
			for i in range(0, maxQueueLen-1):
				prob = poissonProb(advFrac*lambd,i,(siy-queueLen)*t)
				transProb[si][i] = Decimal(prob)
				sumProb = sumProb + Decimal(prob)
			transProb[si][maxQueueLen-1] = Decimal(1)-sumProb

		if siy <= queueLen and siy == six + 1:
			transProb[si][0] = Decimal(1)

	for si in range(2, numStates):
		for sf in range(2, numStates):
			six = si//maxQueueLen
			siy = si%maxQueueLen
			sfx = sf//maxQueueLen
			sfy = sf%maxQueueLen

			if six<siy-1 and six == sfx and siy == sfy-1:
				transProb[si][sf] = Decimal(advFrac)
			if six<siy-1 and siy == sfy and six == sfx-1:
				transProb[si][sf] = Decimal(1-advFrac)


def computeTransProbMine(maxQueueLen, queueLen, lambd, advFrac):

	# These seems correct
	transProb[0][0] = Decimal(1.0-advFrac)
	transProb[0][1] = Decimal(advFrac)
	transProb[maxQueueLen+1][0] = Decimal(1.0)
	transProb[1][maxQueueLen+1] = Decimal(1.0-advFrac)
	transProb[1][2] = Decimal(advFrac)

	# These seems correct
	for si in range(2,numStates):	
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy <= queueLen and siy == six+1:
			transProb[si][0] = Decimal(1.0)

		if siy == maxQueueLen-1 and six < siy-1:
			transProb[si][0] = Decimal(advFrac)

	for si in range(2,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy > queueLen and siy == six+1:
			transProb[si][0] = Decimal(1)

	for si in range(2, numStates):
		for sf in range(2, numStates):
			six = si//maxQueueLen
			siy = si%maxQueueLen
			sfx = sf//maxQueueLen
			sfy = sf%maxQueueLen

			if six<siy-1 and six == sfx and siy == sfy-1:
				transProb[si][sf] = Decimal(advFrac)
			if six<siy-1 and siy == sfy and six == sfx-1:
				transProb[si][sf] = Decimal(1-advFrac)

def checkTransitionMatrixFloat(rowCheck, matrix, numRows, th):
	if rowCheck:
		for i in range(0, numRows):
			rowSum = 0.0
			for j in range(0, numRows):
				rowSum = rowSum + matrix[i][j]
			if rowSum < th:
				print("Too low rowSum for",str(i//maxQueueLen),",",str(i%maxQueueLen), float(rowSum))
				print("Too low rowSum for",i, float(rowSum))
				

def computeExpectedBlocks(lambd, initialCount, tau):
	maxRound = 5
	maxBlock = 50	
	probDist = [[Decimal(0) for x in range(maxBlock)] for y in range(maxRound)] 

	for k in range(0, maxBlock):
		probDist[0][k] =  poissonProb(advFrac*lambd, k, initialCount*tau)

	for i in range(1, maxRound):
		for j in range(0, maxBlock):
			for k in range(0, maxBlock):
				probDist[i][j] = probDist[i][j] +  poissonProb(advFrac*lambd, j, k*tau)*probDist[i-1][k]
	
	expBlockList = [Decimal(0) for x in range(maxRound)]
	expBlocks = Decimal(0.0)
	for i in range(0, maxRound):
		expBlock = Decimal(0)
		for j in range(0, maxBlock):
			expBlock = expBlock + Decimal(j)*probDist[i][j]
		expBlockList[i] = expBlock
		expBlocks = expBlocks + expBlock
	return expBlocks

def computeLateBlocksMine(stationaryProbs, lambd, tau):
	numLateBlocks = Decimal(0.0)
	for si in range(0,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy > queueLen+1 and siy == six + 1:
			totalNumBlocks = siy-(queueLen+1)
			expectedNumBlocks = computeExpectedBlocks(lambd, totalNumBlocks, tau)
			totalNumBlocks = totalNumBlocks + expectedNumBlocks
			numLateBlocks = numLateBlocks + stationaryProbs[si]*Decimal(totalNumBlocks)
	return numLateBlocks

def computeLateBlocksReset(stationaryProbs):
	numLateBlocks = Decimal(0.0)
	for si in range(0,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy > queueLen+1 and siy == six + 1:
			numLateBlocks = numLateBlocks + stationaryProbs[si]*Decimal(siy-queueLen-1)
	return numLateBlocks


def computeProb(n,m):
	term1 = Decimal(1.0)
	term2 = Decimal(1.0)

	for j in range(n,n+m):
		term1 = term1*Decimal(j)/(m-(j-n))*Decimal(advFrac)
		term2 = term2*Decimal(j)/(m-(j-n))*Decimal(1-advFrac)

	for j in range(0,n):
		term1 = term1*Decimal(1-advFrac)
		term2 = term2*Decimal(advFrac)

	return term1-term2


def comuteConfirmationProbsRosen(lambd, low, high, interval):
	confirmProbs = {}
	for numConfirm in range(low, high, interval):
		altProb = Decimal(math.pow(1-advFrac,numConfirm)-math.pow(advFrac,numConfirm))
		for j in range(1,numConfirm):
			altProb = altProb + computeProb(numConfirm,j) 
		confirmProbs[numConfirm] = float(1-altProb)
	return confirmProbs

def computeConfirmtionProbs(stationaryProbs, lambd, tau):
	confirmProbs = {}
	for numConfirm in range(queueLen//2,queueLen, 5):
		numHonesetDeepBlocks = 	stationaryProbs[0]*Decimal(1-advFrac) + stationaryProbs[maxQueueLen+1]*Decimal(1.0)
		numTotalDeepBlocks = 	numHonesetDeepBlocks
		numReplacedBlocks = Decimal(0.0)

		for si in range(0,numStates):
			six = si//maxQueueLen
			siy = si%maxQueueLen
			if siy > numConfirm and siy == six + 1:
				numReplacedBlocks = numReplacedBlocks + (Decimal(six-numConfirm))*stationaryProbs[si]
				totalNumBlocks = siy
				if siy > queueLen:
					if strategy == 'mine':
						totalNumBlocks = totalNumBlocks + computeExpectedBlocks(lambd, totalNumBlocks-queueLen-1, tau)
				numTotalDeepBlocks = numTotalDeepBlocks + (totalNumBlocks + Decimal(six-numConfirm))*stationaryProbs[si]
				numHonesetDeepBlocks = numHonesetDeepBlocks + (Decimal(six-numConfirm))*stationaryProbs[si]
		confirmProbs[numConfirm] = [float(numReplacedBlocks/numHonesetDeepBlocks), float(numReplacedBlocks/numTotalDeepBlocks)]
	return confirmProbs

def computeAdvBlocksMine(stationaryProbs, lambd, tau, acceptProb):
	numAdvBlocks = Decimal(0.0)

	for si in range(2,numStates):
		if si == maxQueueLen + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(acceptProb)
			continue
		six = si//maxQueueLen
		siy = si%maxQueueLen

		if siy <= queueLen+1 and siy == six + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(siy)

		if siy > queueLen+1 and siy == six + 1:
			totalNumBlocks = siy
			expectedNumBlocks =  computeExpectedBlocks(lambd, totalNumBlocks-queueLen-1, tau)
			totalNumBlocks = totalNumBlocks + expectedNumBlocks
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(totalNumBlocks)

		if siy == maxQueueLen-1 and six < siy-1:
			totalNumBlocks = siy
			expectedNumBlocks =  computeExpectedBlocks(lambd, totalNumBlocks-queueLen-1, tau)
			totalNumBlocks = totalNumBlocks + expectedNumBlocks
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(totalNumBlocks)
	return numAdvBlocks

def computeAdvBlocksReset(stationaryProbs, acceptProb):
	numAdvBlocks = Decimal(0.0)
	numAdvBlocks1 = Decimal(0.0)

	for si in range(2,numStates):
		if si == maxQueueLen + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*transProb[maxQueueLen+1][0]*Decimal(acceptProb)
			continue
		six = si//maxQueueLen
		siy = si%maxQueueLen
	
		if siy == six + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(siy)
			continue

		if siy == maxQueueLen-1 and six < siy-1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*transProb[si][0]*Decimal(siy+1)
			
	return numAdvBlocks

def computeHonestBlocksMine(stationaryProbs, lambd, tau, acceptProb):
	numHonestBlocks = stationaryProbs[0]*Decimal(1-advFrac) + stationaryProbs[maxQueueLen+1]*Decimal(1-acceptProb)
	return numHonestBlocks

def computeHonestBlocksReset(stationaryProbs, acceptProb):
	numHonestBlocks = stationaryProbs[0]*transProb[0][0] + stationaryProbs[maxQueueLen+1]*transProb[maxQueueLen+1][0]*Decimal(1-acceptProb)
	return numHonestBlocks

def printTransProb():
	for i in range(0,numStates):
		if i == 0:
			print("X",end="\t")
			for j in range(0, numStates):
				if j in zeroRows:
					continue
				print("("+str(j//maxQueueLen)+","+str(j%maxQueueLen)+")", end="\t")	
			print()

		if i in zeroRows:
			continue
		print("("+str(i//maxQueueLen)+","+str(i%maxQueueLen)+")", end="\t")	
		for j in range(0,numStates):
			if j in zeroRows:
				continue
			print(round(transProb[i][j],2), end="\t")
		print()

def writeStationaryProb(vector, file):
	lenStates = len(vector)
	for i in range(0,lenStates):
		if vector[i] > Decimal(0):
			file.write("("+str(i//maxQueueLen)+","+str(i%maxQueueLen)+"):"+str(round(vector[i], 10))+"\t\t")
			if i%maxQueueLen == maxQueueLen-1:
				file.write("\n")
				for j in range(0, (i+1)//maxQueueLen):
					file.write("\t\t\t\t\t\t")
				if (i+1)//maxQueueLen > 1:
					file.write("\t\t\t\t\t\t")

def writeRawStationaryProb(vector, file):
	file.write(str(vector))
	file.write("\n\n")
	file.write("[")
	for i in range(numStates):
		file.write(str(float(vector[i]))+",")	
	file.write("]")
	file.write("\n\n")
	
def writeExperimentInfo(strategy, file):
	file.write("Strategy of Adversary: "+strategy+"\n")
	file.write("Fraction of Adversary: "+str(advFrac)+"\n")
	file.write("Global Arrival Rate: "+str(globalLambda)+"\n")
	file.write("tau: "+str(tau)+"\n")
	file.write("Thresholds: "+str(stationaryTh)+"\n")
	file.write("--------------------------------------------------------\n")
	file.write("queueLen,maxQueueLen,numItr,lateRaw,honestRaw,advRaw,lateFrac,honestFrac,advFrac\n")

def printExperimentInfo(strategy):
	print("Strategy of Adversary: "+strategy)
	print("Fraction of Adversary: "+str(advFrac))
	print("tau: "+str(tau))
	print("Global Inter arrival: "+str(1/globalLambda))
	print("Thresholds: "+str(stationaryTh))
	print("----------------------------------------------")
	print("queueLen,maxQueueLen,numItr,lateRaw,honestRaw,advRaw,lateFrac,honestFrac,advFrac")

def writeResults(file):
	file.write(str(queueLen)+","+str(maxQueueLen-1)+","+str(numitr)+","+str(numLateBlocks)+","+str(numHonestBlocks)+","+str(numAdvBlocks)+","+str(lateFraction)+","+str(honestFraction)+","+str(advFraction)+"\n")
	file.close()

def printResults():
	numitr = 10
	print(str(queueLen)+","+str(maxQueueLen-1)+","+str(numitr)+","+str(numLateBlocks)+","+str(numHonestBlocks)+","+str(numAdvBlocks)+","+str(lateFraction)+","+str(honestFraction)+","+str(advFraction))	

def readStationaryProb(fileName):
	kList = []
	stationaryResults = {}

	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()
		dataLen = len(data)
		index=0

		while index < dataLen:
			content = data[index].strip().split('-')
			if content[0] == 'Q':
				k = int(content[1])
				kList.append(k)
				index = index + 1
				info = data[index].strip()
				statProbStr = info[1:-2].split(',')
				numStates = len(statProbStr)
				statProb = []
				for j in range(0,numStates):
					statProb.append(Decimal(statProbStr[j]))
				index = index+1
				stationaryResults[k] = statProb
		return kList, stationaryResults
	else:
		print("File ", fileName, "not found to read stationary probs")

if len(sys.argv) < 2:
	print("\n mine \n reset\n")
	exit()

strategy = sys.argv[1]
if strategy != 'mine' and strategy != 'reset':
	print("\n mine \n reset\n")
	exit()

advFrac = 1/3.0
stationaryTh = 10**(-9)
checkMatrixTh = 1-10**(-15)
honestLambda = 1/15.0
globalLambda = honestLambda/(1-advFrac)
tau = 5

outputFilePath = os.environ["HOME"]+"/EVD-Expt/data0/replaced-"+str(strategy)+".txt"
outputFile = open(outputFilePath, 'a+')
# printExperimentInfo(strategy)

inputFilePath = os.environ["HOME"]+"/EVD-Expt/data0/stat-dist-mine.dat"
kList, stationaryResults = readStationaryProb(inputFilePath)

for k in kList:
	queueLen = k
	maxQueueLen = k+35+1
	numStates = maxQueueLen*maxQueueLen
	probs = stationaryResults[k]
	transProb = [[Decimal(0) for x in range(numStates)] for y in range(numStates)] 
	zeroRows = []

	if strategy =='mine':
		computeTransProbMine(maxQueueLen, queueLen, globalLambda, advFrac)
	else:
		computeTransProbReset(maxQueueLen, queueLen, globalLambda, advFrac, tau)
	checkTransitionMatrix(True, transProb, numStates, checkMatrixTh)
	
	acceptProb = 1.0
	numLateBlocks = 0.0
	numAdvBlocks = 0.0
	numHonestBlocks = 0.0

	confirmProbs = {}
	if strategy =='mine':
		numLateBlocks = float(computeLateBlocksMine(probs, globalLambda, tau))
		numAdvBlocks = float(computeAdvBlocksMine(probs, globalLambda, tau, acceptProb))
		numHonestBlocks = float(computeHonestBlocksMine(probs, globalLambda, tau, acceptProb))		
	else:
		numLateBlocks = float(computeLateBlocksReset(probs))
		numAdvBlocks = float(computeAdvBlocksReset(probs, acceptProb))
		numHonestBlocks = float(computeHonestBlocksReset(probs, acceptProb))

	confirmProbs = computeConfirmtionProbs(probs, globalLambda, tau)
	lateFraction = numLateBlocks/(numAdvBlocks + numHonestBlocks)
	advFraction = numAdvBlocks/(numAdvBlocks + numHonestBlocks)
	honestFraction = numHonestBlocks/(numAdvBlocks + numHonestBlocks)

	printResults()
	# outputFile = open(outputFilePath, 'a+')
	# writeResults(outputFile)
	confirmProbs2 = comuteConfirmationProbsRosen(globalLambda,queueLen//2,queueLen, 5)

	print(confirmProbs)
	print()
	print(confirmProbs2)
	del stationaryResults[k]
	transProb = []