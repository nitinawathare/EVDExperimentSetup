'''
This file computes the success probability
of an attacker performing an hidden chain
attack. We use discrete event simulation to
get this probability.
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

#Compute the probability of k events in a time interval of
#size t with parameter lambda
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

def computeTransProbReset(maxQueueLen, queueLen, lambd, advFrac, t):

	# These seems correct
	transProb[0][0] = Decimal(1.0-advFrac)	# (0,0) -> (0,0)
	transProb[0][1] = Decimal(advFrac)	# (0,0) -> (0,1)
	transProb[maxQueueLen+1][0] = Decimal(1.0)	# (1,1) -> (0,0)
	transProb[1][maxQueueLen+1] = Decimal(1.0-advFrac)	# (0,1) -> (1,1)
	transProb[1][2] = Decimal(advFrac) # (0,1) -> (0,2)


	for si in range(2,numStates):	
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy <= queueLen and siy == six+1:	# y<=k and y=x+1
			transProb[si][0] = Decimal(1.0)

		if siy == maxQueueLen-1 and six < siy-1:	# y=M and x<y-1
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

		# if siy <= queueLen and siy == six + 1:	
		# 	transProb[si][0] = Decimal(1)

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

#Compute transition probability for MAR attack
def computeTransProbMine(maxQueueLen, queueLen, lambd, advFrac):

	# initialize the transition probability for states.
	transProb[0][0] = Decimal(1.0-advFrac) # (0,0) -> (0,0)
	transProb[0][1] = Decimal(advFrac) # (0,0) -> (0,1)
	transProb[maxQueueLen+1][0] = Decimal(1.0) # (0,0) -> (1,1)
	transProb[1][maxQueueLen+1] = Decimal(1.0-advFrac) # (0,1) -> (1,1)
	transProb[1][2] = Decimal(advFrac) # (0,1) -> (0,2)


	# For states of the form (0,2) and beyond
	for si in range(2,numStates):	
		six = si//maxQueueLen #row number
		siy = si%maxQueueLen #column number

		if siy <= queueLen and siy == six+1:	# if y<=k and y = x+1
			transProb[si][0] = Decimal(1.0)

		if siy == maxQueueLen-1 and six < siy-1:	# y==M and x<y-1
			transProb[si][0] = Decimal(advFrac)

	# For states starting from (0,2) and beyond
	for si in range(2,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen

		if siy > queueLen and siy == six+1:	# if y>k and y=x+1 
			transProb[si][0] = Decimal(1)

	# For states starting from (0,2) and beyond
	for si in range(2, numStates):
		for sf in range(2, numStates):
			six = si//maxQueueLen
			siy = si%maxQueueLen
			sfx = sf//maxQueueLen
			sfy = sf%maxQueueLen

			if six<siy-1 and six == sfx and siy == sfy-1:  # if x<y-1, x=x', y'=y+1
				transProb[si][sf] = Decimal(advFrac)
			if six<siy-1 and siy == sfy and six == sfx-1:	# if x<y-1, y=y' and x'=x+1
				transProb[si][sf] = Decimal(1-advFrac)

def vectorMatrixMul(vector, matrix):
	numRows = len(vector)
	resultVector = []
	for j in range(0, numRows):
		result = Decimal(0.0)
		if j in zeroRows:
			resultVector.append(result)
		else:
			for i in range(0, numRows):
				result = result + Decimal(vector[i]*matrix[i][j])
			resultVector.append(result)
	return resultVector

def abs(x):
	if x<0:
		return (-1)*x
	else:
		return x

def computeRelDifference(newVector, oldVector):
	numRows = len(newVector)
	maxRelChange = 0.0
	for i in range(0, numRows):
		if i in zeroRows:
			continue
		relChange = (newVector[i]-oldVector[i])/oldVector[i]
		relChange = abs(relChange)
		if relChange > maxRelChange:
			maxRelChange = relChange
	return maxRelChange


def computeAbsDifference(newVector, oldVector):
	numRows = len(newVector)
	maxAbsChange = 0.0
	for i in range(0, numRows):
		if i in zeroRows:
			continue
		absChange = abs(newVector[i]-oldVector[i])
		if absChange > maxAbsChange:
			maxAbsChange = absChange
	return maxAbsChange

def computeStationaryProb(matrix, th, size):
	intialVector = [Decimal(1.0)]*size
	prevVector = intialVector
	difference = Decimal(1.0)
	it= 0.0
	while difference > th:
		currVector = vectorMatrixMul(prevVector, matrix)
		difference = computeAbsDifference(currVector, prevVector)
		prevVector = currVector
		it = it+1
		if it%1000==0:
			print(it, float(difference))
			# break
	prevVector = [x/sum(prevVector) for x in prevVector]
	return (it, prevVector)

def checkTransitionMatrix(rowCheck, matrix, numRows, th):
	if rowCheck:
		for i in range(0, numRows):
			rowSum = Decimal(0.0)
			for j in range(0, numRows):
				rowSum = rowSum + matrix[i][j]
			# if rowSum < th:
			# 	print("Too low rowSum for",str(i//maxQueueLen),",",str(i%maxQueueLen), float(rowSum))
				# print("Too low rowSum for",i, float(rowSum))
			if rowSum == 0:
				zeroRows.append(i)
				

	else:
		for i in range(0, numRows):
			colSum = Decimal(0.0)
			for j in range(0, numRows):
				colSum = colSum + matrix[j][i]
			if colSum == 0:
				# print("Too low colSum for",str(i//maxQueueLen),",",str(i%maxQueueLen), float(colSum))
				print("Too low colSum for",i, float(colSum))

def checkTransitionMatrixFloat(rowCheck, matrix, numRows, th):
	if rowCheck:
		for i in range(0, numRows):
			rowSum = 0.0
			for j in range(0, numRows):
				rowSum = rowSum + matrix[i][j]
			if rowSum < th:
				print("Too low rowSum for",str(i//maxQueueLen),",",str(i%maxQueueLen), float(rowSum))
				print("Too low rowSum for",i, float(rowSum))
				

	else:
		for i in range(0, numRows):
			colSum = 0.0
			for j in range(0, numRows):
				colSum = colSum + matrix[j][i]
			if colSum == 0:
				print("Too low colSum for",str(i//maxQueueLen),",",str(i%maxQueueLen), float(colSum))
				# print("Too low colSum for",i, float(colSum))

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


def computeAdvBlocksMine(stationaryProbs, lambd, tau, acceptProb):
	numAdvBlocks = Decimal(0.0)
	numAdvBlocks1 = Decimal(0.0)

	for si in range(2,numStates):
		if si == maxQueueLen + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*transProb[maxQueueLen+1][0]*Decimal(acceptProb)
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
	numHonestBlocks = stationaryProbs[0]*transProb[0][0] + stationaryProbs[maxQueueLen+1]*transProb[maxQueueLen+1][0]*Decimal(1-acceptProb)
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
	file.write("queueLen,maxQueueLen,numItr,lateRaw,honestRaw,advRaw,lateFrac,honestFrac,advFrac,emptyFrac,time\n")

def printExperimentInfo(strategy):
	print("Strategy of Adversary: "+strategy)
	print("Fraction of Adversary: "+str(advFrac))
	print("tau: "+str(tau))
	print("Global Inter arrival: "+str(1/globalLambda))
	print("Thresholds: "+str(stationaryTh))
	print("----------------------------------------------")
	print("queueLen,maxQueueLen,numItr,lateRaw,honestRaw,advRaw,lateFrac,honestFrac,advFrac,emptyFrac,time")

def writeResults(file):
	file.write(str(queueLen)+","+str(maxQueueLen-1)+","+str(numitr)+","+str(numLateBlocks)+","+str(numHonestBlocks)+","+str(numAdvBlocks)+","+str(lateFraction)+","+str(honestFraction)+","+str(advFraction)+","+str(emptyFraction)+","+str(timeTaken)+"\n")
	file.close()

def printResults():
	print(str(queueLen)+","+str(maxQueueLen-1)+","+str(numitr)+","+str(numLateBlocks)+","+str(numHonestBlocks)+","+str(numAdvBlocks)+","+str(lateFraction)+","+str(honestFraction)+","+str(advFraction)+","+str(emptyFraction)+","+str(timeTaken))

'''
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

#Check command line arguments for which strategy to consider
if len(sys.argv) < 2:
	print("\n mine \n reset\n")
	exit()

#On invalid input suggest input
advStrategy = sys.argv[1]
if advStrategy != 'mine' and advStrategy != 'reset':
	print("\n mine \n reset\n")
	exit()

advFrac = 1/3.0
stationaryTh = 10**(-9)
checkMatrixTh = 1-10**(-15)
honestLambda = 1/15.0
globalLambda = honestLambda/(1-advFrac)
tau = 5

outputFilePath = os.environ["HOME"]+"/EVD-Expt/data/theo/hidden-"+str(advStrategy)+".txt"
outputFile = open(outputFilePath, 'a+')
outputFilePathRaw = os.environ["HOME"]+"/EVD-Expt/data/theo/hidden-raw-"+str(advStrategy)+".txt"
outputFileRaw = open(outputFilePathRaw, 'a+')
printExperimentInfo(advStrategy)
writeExperimentInfo(advStrategy, outputFile)
writeExperimentInfo(advStrategy, outputFileRaw)

for k in range(10,35,10):
	queueLen = k
	maxQueueLen = k+25+1
	numStates = maxQueueLen*maxQueueLen
	transProb = [[Decimal(0) for x in range(numStates)] for y in range(numStates)] 
	zeroRows = []

	if advStrategy =='mine':
		computeTransProbMine(maxQueueLen, queueLen, globalLambda, advFrac)
	else:
		computeTransProbReset(maxQueueLen, queueLen, globalLambda, advFrac, tau)
	
	checkTransitionMatrix(True, transProb, numStates, checkMatrixTh)
	startTime = time.clock()
	numitr, probs = computeStationaryProb(transProb,stationaryTh, numStates)
	endTime = time.clock()
	timeTaken = endTime-startTime

	acceptProb = 1.0
	numLateBlocks = 0.0
	numAdvBlocks = 0.0
	numHonestBlocks = 0.0

	'''
	We are interested in computing the fraction of empty blocks that the
	honest miners will mine. The argument we would like to give here is
	that, honest miner mines empty block as long as blocks entering
	the queue of the honest miners are late. Also, only adversarial
	late blocks enter the queue. So for any given strategy, expected
	fraction of empty honest blocks will be simply:
		= alpha/beta*(fraction of late blocks)
	Hence, we don't have to make any changes in the Markov chain analysis.
	'''

	if advStrategy =='mine':
		numLateBlocks = float(computeLateBlocksMine(probs, globalLambda, tau))
		numAdvBlocks = float(computeAdvBlocksMine(probs, globalLambda, tau, acceptProb))
		numHonestBlocks = float(computeHonestBlocksMine(probs, globalLambda, tau, acceptProb))
	else:
		numLateBlocks = float(computeLateBlocksReset(probs))
		numAdvBlocks = float(computeAdvBlocksReset(probs, acceptProb))
		numHonestBlocks = float(computeHonestBlocksReset(probs, acceptProb))
	

	lateFraction = numLateBlocks/(numAdvBlocks + numHonestBlocks)
	advFraction = numAdvBlocks/(numAdvBlocks + numHonestBlocks)
	honestFraction = numHonestBlocks/(numAdvBlocks + numHonestBlocks)
	emptyFraction = ((1-advFrac)/advFrac)*(lateFraction)

	printResults()
	outputFile = open(outputFilePath, 'a+')
	writeResults(outputFile)
	outputFileRaw = open(outputFilePathRaw, 'a+')
	writeRawStationaryProb(probs, outputFileRaw)
	writeResults(outputFileRaw)
