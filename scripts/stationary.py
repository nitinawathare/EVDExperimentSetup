'''

This file computes the stationary
probability in the case with increasing
block processing time, with both honest
miners and with an adversary trying to 
skip block processing.

'''

import sys
import math 
import numpy as np
import matplotlib.pyplot as plt

from decimal import *
getcontext().prec = 400

def poissonProb(lambd, k, t):
	nTerm1 = Decimal(math.pow(Decimal(lambd*t), Decimal(k)))
	nTerm2 = Decimal(np.exp(-1*(lambd*t)))
	dTerm1 = Decimal(math.factorial(k))

	return nTerm1*nTerm2/dTerm1

def nProb(lambdx, lambdy, t):
	term1 = Decimal(lambdx)/Decimal(lambdx+lambdy)
	term2 = Decimal(1.0)-Decimal(np.exp((-1)*(lambdx+lambdy)*t))

	return term1*term2

def vectorMatrixMul(vector, matrix):
	numRows = len(vector)
	resultVector = []
	for j in range(0, numRows):
		result = Decimal(0.0)
		for i in range(0, numRows):
			result = result + vector[i]*matrix[i][j]
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
		relChange = (newVector[i]-oldVector[i])/oldVector[i]
		relChange = abs(relChange)
		if relChange > maxRelChange:
			maxRelChange = relChange
	return maxRelChange


def computeAbsDifference(newVector, oldVector):
	numRows = len(newVector)
	maxAbsChange = 0.0
	for i in range(0, numRows):
		absChange = abs(newVector[i]-oldVector[i])
		# absChange = abs(absChange)
		if absChange > maxAbsChange:
			maxAbsChange = absChange
	return maxAbsChange


def computeHonestStationaryProb(matrix, th):
	intialVector = [Decimal(1.0)]*numNodes
	prevVector = intialVector
	difference = Decimal(1.0)
	it= 0.0
	while difference > th:
		currVector = vectorMatrixMul(prevVector, matrix)
		difference = computeAbsDifference(currVector, prevVector)
		prevVector = currVector
		it = it+1
		if it%10 == 0:
			print(it, float(difference))
	prevVector = [x/sum(prevVector) for x in prevVector]
	return (it, prevVector)

def computeSkipStationaryProb(matrix, th):
	intialVector = [Decimal(1.0)]*numNodes
	prevVector = intialVector
	difference = Decimal(1.0)
	it= 0.0
	while difference > th:
		currVector = vectorMatrixMul(prevVector, matrix)
		difference = computeAbsDifference(currVector, prevVector)
		prevVector = currVector
		it = it+1
		if it%10 == 0:
			print(it, float(difference))
	prevVector = [x/sum(prevVector) for x in prevVector]
	return (it, prevVector)

def computeHonestTransition(t, gLambd):
	for i in range(0, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		for j in range(0, numNodes):
			transProb = Decimal(0.0)
			probj = initProb[j]
			lambdj = probj*gLambd
			if i == j:
				term0 = poissonProb(lambdi, 0, t)
				termNon0 = Decimal(1.0)-term0
				transProb = termNon0 + Decimal(probi)*term0
				honestTranstion[i][j] = transProb
			else:
				term0 = poissonProb(lambdi, 0, t)
				transProb = Decimal(probj)*term0
				honestTranstion[i][j] = transProb

def computeSkipTransition(t, gLambd):

	# Computing p(1,1)
	advProb = initProb[0]
	advLambd = advProb*gLambd
	term0 = poissonProb(advLambd, 0, t)
	termNon0 = Decimal(1.0)- term0
	transProb00 = termNon0 + Decimal(advProb)*term0
	skipTranstion[0][0] = transProb00

	# computing p(1,j)
	for j in range(1, numNodes):
		probj = initProb[j]
		term0 = poissonProb(advLambd, 0, t)
		transProb = Decimal(probj)*term0
		skipTranstion[0][j] = transProb

	# computing p(i,1)
	for i in range(1, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		term0 = poissonProb(advLambd+lambdi, 0, t)
		nprob = nProb(advLambd, lambdi, t)
		transProb = nprob + Decimal(advProb)*term0 
		skipTranstion[i][0] = transProb

	# computing the rest
	for i in range (1, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		for j in range(1, numNodes):
			# computing p(i,i) for i!= 1
			if i==j: 
				nprob = nProb(lambdi, advLambd, t)
				term0 = poissonProb(advLambd+lambdi, 0, t)
				transProb = nprob + Decimal(probi)*term0
				skipTranstion[i][j] = transProb
			# computing p(i,j) for i!=j!=1
			else:
				probj = initProb[j]
				term0 = poissonProb(advLambd+lambdi, 0, t)
				transProb = Decimal(probj)*term0
				skipTranstion[i][j] = transProb



def checkTransitionMatrix(rowCheck, matrix, numRows, th):
	if rowCheck:
		for i in range(0, numRows):
			rowSum = Decimal(0.0)
			for j in range(0, numRows):
				rowSum = rowSum + matrix[i][j]
			if rowSum < th:
				print("Too low rowSum for",i, float(rowSum))


initProb = [0.3297630187360915, 0.16161252867434858, 0.15059349262825678, 0.05715206695815737, 0.056711305516792994, 0.04407614418436712, 0.04143157553318527, 0.03526091534709429, 0.026078385308518044, 0.018365060077152478, 0.013421185904173738, 0.013222843254910724, 0.01248824085230392, 0.010504814363667899, 0.008080626433667502, 0.005939260428950312, 0.0015793951668028662, 0.0011019036049087372, 0.0008815228837272837, 0.0008741768594216269, 0.000844792763197531, 0.0008080626436663093, 0.0008080626436663093, 0.0007346024026068043, 0.0007346024026068043, 0.0006244120430146082, 0.0005876819224848558, 0.0005876819224848558, 0.0005771036480039461, 0.00044076144136437643, 0.00036730120130340217, 0.00036730120130340217, 0.00036730120130340217, 0.00035995517799627627, 0.00035995517799627627, 0.0002277267444885795, 0.0001542665044276052, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853]

processTime = [4]
recipLambd = 15.0
globalLambd = 1.0/recipLambd
numNodes = len(initProb)
checkMatrixTh = 1-10**(-15)
stationaryTh = 10**(-14)

honestTranstion = [[0]*numNodes]*numNodes
skipTranstion = [[0]*numNodes]*numNodes

honestResults = {}
honestResultsExtended = {}

skipResults = {}
skipResultsExtended = {}


processTime = [0.0, 0.2, 0.5, 1, 2, 4]
for t in processTime:
	computeHonestTransition(t, globalLambd)
	checkTransitionMatrix(True, honestTranstion, numNodes, checkMatrixTh)
	numitr, probs = computeHonestStationaryProb(honestTranstion, stationaryTh)
	honestResultsExtended[t] = float(probs[0])


	computeSkipTransition(2*t, globalLambd)
	checkTransitionMatrix(True, skipTranstion, numNodes, checkMatrixTh)
	numitr, probs = computeSkipStationaryProb(skipTranstion, stationaryTh)
	skipResultsExtended[t] = float(probs[0])


for t in processTime:
	globalLambd = 1.0/(recipLambd-2*t)

	computeHonestTransition(t, globalLambd)
	checkTransitionMatrix(True, honestTranstion, numNodes, checkMatrixTh)
	numitr, probs = computeHonestStationaryProb(honestTranstion, stationaryTh)
	honestResults[t] = float(probs[0])


	computeSkipTransition(2*t, globalLambd)
	checkTransitionMatrix(True, skipTranstion, numNodes, checkMatrixTh)
	numitr, probs = computeSkipStationaryProb(skipTranstion, stationaryTh)
	skipResults[t] = float(probs[0])

# computeSkipTransition(4, globalLambd)
# numitr, probs = computeSkipStationaryProb(skipTranstion, stationaryTh)

file = open('/home/sourav/EVD-Expt/stationary.csv', 'w+')
file.write("hE,h,sE,s\n")
for t in processTime:
	file.write(str(t)+","+str(honestResultsExtended[t])+","+str(honestResults[t])+","+str(skipResultsExtended[t])+","+str(skipResults[t])+"\n")

# print()
# for t in processTime:
# 	print(t, honestResultsExtended[t])

# print()
# for t in processTime:
# 	print(t, skipResults[t])

# print()
# for t in processTime:
# 	print(t, skipResultsExtended[t])


# computeSkipTransition(1, globalLambd)
# checkTransitionMatrix(False, skipTranstion, numNodes, checkMatrixTh)