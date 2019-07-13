'''
This file computes the success probability
of an attacker performing an hidden chain
attack. 

'''
import sys
import time
import math 
import numpy as np
import os
# import matplotlib.pyplot as plt

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
		sumProb = Decimal(0.0)
		if siy > queueLen and siy == six+1:
			transProb[si][0] = Decimal(1)-sumProb

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

def computeLateBlocksMine(stationaryProbs, lambd, tau):
	numLateBlocks = Decimal(0.0)
	for si in range(0,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy > queueLen and siy == six + 1:
			totalNumBlocks = siy-queueLen
			expectedNumBlocks =  advFrac*lambd*(siy-queueLen)*tau
			totalNumBlocks = totalNumBlocks + expectedNumBlocks
	
			while expectedNumBlocks > 10**(-10):
				expectedNumBlocks = advFrac*lambd*expectedNumBlocks*tau
				totalNumBlocks = totalNumBlocks + expectedNumBlocks
	
			print(siy-queueLen, totalNumBlocks)
			numLateBlocks = numLateBlocks + stationaryProbs[si]*Decimal(totalNumBlocks)
	return numLateBlocks

def computeLateBlocksReset(stationaryProbs):
	numLateBlocks = Decimal(0.0)
	for si in range(0,numStates):
		six = si//maxQueueLen
		siy = si%maxQueueLen
		if siy > queueLen and siy == six + 1:
			numLateBlocks = numLateBlocks + stationaryProbs[si]*Decimal(siy-queueLen)
	return numLateBlocks


def computeAdvBlocksMine(stationaryProbs, lambd, tau, acceptProb):
	numAdvBlocks = Decimal(0.0)
	numAdvBlocks1 = Decimal(0.0)

	for si in range(2,numStates):
		if si == maxQueueLen + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*transProb[maxQueueLen+1][0]*Decimal(acceptProb)
			# numAdvBlocks1 = numAdvBlocks1 + Decimal(acceptProb)
			continue
		six = si//maxQueueLen
		siy = si%maxQueueLen

		if siy <= queueLen and siy == six + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(siy)

		if siy > queueLen and siy == six + 1:
			totalNumBlocks = siy
			expectedNumBlocks =  advFrac*lambd*(siy-queueLen)*tau
			totalNumBlocks = totalNumBlocks + expectedNumBlocks
			
			while expectedNumBlocks > 10**(-10):
				expectedNumBlocks = advFrac*lambd*expectedNumBlocks*tau
				totalNumBlocks = totalNumBlocks + expectedNumBlocks
	
			print(siy-queueLen, totalNumBlocks)
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(totalNumBlocks)

		if siy == maxQueueLen-1 and six < siy-1:
			totalNumBlocks = siy
			expectedNumBlocks =  advFrac*lambd*(siy-queueLen)*tau
			totalNumBlocks = totalNumBlocks + expectedNumBlocks
			
			while expectedNumBlocks > 10**(-10):
				expectedNumBlocks = advFrac*lambd*expectedNumBlocks*tau
				totalNumBlocks = totalNumBlocks + expectedNumBlocks
	
			print(siy-queueLen, totalNumBlocks)
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(totalNumBlocks)
			# numAdvBlocks1 = numAdvBlocks1 + Decimal(siy)

	# print("a:",numAdvBlocks1)
	return numAdvBlocks

def computeAdvBlocksReset(stationaryProbs, acceptProb):
	numAdvBlocks = Decimal(0.0)
	numAdvBlocks1 = Decimal(0.0)

	for si in range(2,numStates):
		if si == maxQueueLen + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*transProb[maxQueueLen+1][0]*Decimal(acceptProb)
			# numAdvBlocks1 = numAdvBlocks1 + Decimal(acceptProb)
			continue
		six = si//maxQueueLen
		siy = si%maxQueueLen
	
		if siy == six + 1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*Decimal(siy)
			# numAdvBlocks1 = numAdvBlocks1 + Decimal(siy)
			continue

		if siy == maxQueueLen-1 and six < siy-1:
			numAdvBlocks = numAdvBlocks + stationaryProbs[si]*transProb[si][0]*Decimal(siy+1)
			# numAdvBlocks1 = numAdvBlocks1 + Decimal(siy)

	# print("a:",numAdvBlocks1)
	return numAdvBlocks

def computeHonestBlocksMine(stationaryProbs, lambd, tau, acceptProb):
	numHonestBlocks = stationaryProbs[0]*transProb[0][0] + stationaryProbs[maxQueueLen+1]*transProb[maxQueueLen+1][0]*Decimal(1-acceptProb)
	# numHonestBlocks1 = Decimal(1) + Decimal(1-acceptProb)
	# print("h::", numHonestBlocks1)
	return numHonestBlocks

def computeHonestBlocksReset(stationaryProbs, acceptProb):
	numHonestBlocks = stationaryProbs[0]*transProb[0][0] + stationaryProbs[maxQueueLen+1]*transProb[maxQueueLen+1][0]*Decimal(1-acceptProb)
	# numHonestBlocks1 = Decimal(1) + Decimal(1-acceptProb)
	# print("h::", numHonestBlocks1)
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
	

def writeExperimentInfo(strategy):
	outputFile.write("Strategy of Adversary: "+strategy+"\n")
	outputFile.write("Fraction of Adversary: "+str(advFrac)+"\n")
	outputFile.write("Global Arrival Rate: "+str(globalLambda)+"\n")
	outputFile.write("Allowable Length of Queue: "+str(queueLen)+"\n")
	outputFile.write("Maximum Queue length: "+str(maxQueueLen-1)+"\n")
	outputFile.write("Number of Iterations: "+str(numitr)+"\n")
	outputFile.write("Time Taken: "+str(timeTaken)+"\n")
	outputFile.write("Thresholds: "+str(stationaryTh)+"\n\n")

	outputFile.write("late: "+str(numLateBlocks)+","+str(lateFraction)+"\n")
	outputFile.write("adv: "+str(numAdvBlocks)+","+str(advFraction)+"\n")
	outputFile.write("honest: "+str(numHonestBlocks)+","+str(honestFraction)+"\n\n")

def printExperimentInfo(strategy):
	print("Strategy of Adversary: "+strategy)
	print("Fraction of Adversary: "+str(advFrac))
	print("Global Inter arrival: "+str(1/globalLambda))
	print("Allowable Length of Queue: "+str(queueLen))
	print("Maximum Queue length: "+str(maxQueueLen-1))
	print("Number of Iterations: "+str(numitr))
	print("Time Taken: "+str(timeTaken))
	print("Thresholds: "+str(stationaryTh))
	print()
	print("late", numLateBlocks, lateFraction)
	print("adv", numAdvBlocks, advFraction)
	print("honest", numHonestBlocks, honestFraction)


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

advFrac = 1/3.0
queueLen = 3
maxQueueLen = 5 + 1
stationaryTh = 10**(-9)
checkMatrixTh = 1-10**(-15)
honestLambda = 1/15.0
globalLambda = honestLambda + (advFrac/(1-advFrac))*honestLambda
tau = 5
numStates = maxQueueLen*maxQueueLen
transProb = [[Decimal(0) for x in range(numStates)] for y in range(numStates)] 
zeroRows = []

if len(sys.argv) < 2:
	print("\n mine \n reset\n")
	exit()

advStrategy = sys.argv[1]
print("Started Computing Transition Probability...")
if advStrategy =='mine':
	computeTransProbMine(maxQueueLen, queueLen, globalLambda, advFrac)
elif advStrategy == 'reset':
	computeTransProbReset(maxQueueLen, queueLen, globalLambda, advFrac, tau)
else:
	print("\n mine \n reset\n")
	exit()
print("Finished Computing Transition Probability...")

checkTransitionMatrix(True, transProb, numStates, checkMatrixTh)
print("Started Computing Stationary Probability...")
startTime = time.clock()
numitr, probs = computeStationaryProb(transProb,stationaryTh, numStates)
endTime = time.clock()
print("Finished Computing Stationary Probability...")
timeTaken = endTime-startTime

acceptProb = 1.0
numLateBlocks = 0.0
numAdvBlocks = 0.0
numHonestBlocks = 0.0


if advStrategy =='mine':
	numLateBlocks = float(computeLateBlocksMine(probs, globalLambda, tau))
	numAdvBlocks = float(computeAdvBlocksMine(probs, globalLambda, tau, acceptProb))
	numHonestBlocks = float(computeHonestBlocksMine(probs, globalLambda, tau, acceptProb))
elif advStrategy == 'reset':
	numLateBlocks = float(computeLateBlocksReset(probs))
	numAdvBlocks = float(computeAdvBlocksReset(probs, acceptProb))
	numHonestBlocks = float(computeHonestBlocksReset(probs, acceptProb))
else:
	print("\n mine \n reset\n")
	exit()

lateFraction = numLateBlocks/(numAdvBlocks + numHonestBlocks)
advFraction = numAdvBlocks/(numAdvBlocks + numHonestBlocks)
honestFraction = numHonestBlocks/(numAdvBlocks + numHonestBlocks)

outputFilePath = os.environ["HOME"]+'/EVD-Expt/data/hidden.csv'
outputFile = open(outputFilePath, 'a+')
printExperimentInfo(advStrategy)
writeExperimentInfo(advStrategy)
writeRawStationaryProb(probs, outputFile)
outputFile.write("--------------------------------------------------------\n\n")




