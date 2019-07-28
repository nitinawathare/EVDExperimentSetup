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

def computeStationaryProb(matrix, th):
	intialVector = [Decimal(1.0)]*numNodes
	prevVector = intialVector
	difference = Decimal(1.0)
	it= 0.0
	while difference > th:
		currVector = vectorMatrixMul(prevVector, matrix)
		difference = computeAbsDifference(currVector, prevVector)
		prevVector = currVector
		it = it+1
		# if it%10 == 0:
		# 	print(it, float(difference))
	prevVector = [x/sum(prevVector) for x in prevVector]
	return (it, prevVector)

def computeHonestTransitionFast(t, c, gLambd):
	advProb = initProb[0]
	advLambd = advProb*gLambd
	for i in range(0, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		for j in range(0, numNodes):
			transProb = Decimal(0.0)
			probj = initProb[j]
			lambdj = probj*gLambd
			if i == 0:
				term0 = poissonProb(lambdi, 0, 2*t-c*t)
				termNon0 = 1-term0
				if i == j:
					transProb = termNon0 + term0*Decimal(probi)
				else:
					transProb = term0*Decimal(probj) 
			else:
				if j == 0:
					term0 = poissonProb(advLambd,0, t-2*c*t)
					termNon0 = 1-term0
					nprob1i = nProb(advLambd, lambdi, 2*t-t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t -t)
					transProb = termNon0  + term0*(nprob1i + term01i*Decimal(advProb))
				elif i == j:
					term0 = poissonProb(advLambd,0,t-2*c*t)
					nprobi1 = nProb(lambdi, advLambd, 2*t-t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t -t)
					transProb = term0*(nprobi1 + term01i*Decimal(probi))
				else:
					term0 = poissonProb(advLambd, 0, t-2*c*t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t -t)
					transProb = Decimal(probj)*term0*term01i
			honestTranstion[i][j] = transProb

def computeHonestTransitionSlow(t, c, gLambd):
	advProb = initProb[0]
	advLambd = advProb*gLambd
	for i in range(0, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		for j in range(0, numNodes):
			transProb = Decimal(0.0)
			probj = initProb[j]
			lambdj = probj*gLambd
			if i == 0:
				term0 = poissonProb(lambdi, 0, 2*t-c*t)
				termNon0 = 1-term0
				if i == j:
					transProb = termNon0 + term0*Decimal(probi)
				else:
					transProb = term0*Decimal(probj)
			else:
				if j == 0:
					term0 = poissonProb(lambdi, 0, 2*c*t - t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t-2*c*t)
					nprob1i = nProb(advLambd, lambdi, 2*t-2*c*t)
					transProb = term0*(nprob1i + term01i*Decimal(advProb))
				elif i == j:
					term0 = poissonProb(lambdi, 0, 2*c*t-t)
					termNon0 = Decimal(1.0)-term0
					nprobi1 = nProb(lambdi,advLambd, 2*t-2*c*t)
					term01i = poissonProb(lambdi+advLambd, 0, 2*t-2*c*t)
					transProb = termNon0 + term0*(nprobi1 + term01i*Decimal(probi))
				else:
					term0 = poissonProb(lambdi, 0, 2*c*t-t)
					term01i = poissonProb(lambdi+advLambd, 0, 2*t-2*c*t)
					transProb = Decimal(probj)*term0*term01i
			honestTranstion[i][j] = transProb

def computeSkipCreateTransition(t, c, gLambd):
	advProb = initProb[0]
	advLambd = advProb*gLambd
	for i in range(0, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		for j in range(0, numNodes):
			transProb = Decimal(0.0)
			probj = initProb[j]
			lambdj = probj*gLambd
			if i == 0:
				term0 = poissonProb(lambdi, 0, 2*t)
				termNon0 = 1-term0
				if i == j:
					transProb = termNon0 + term0*Decimal(probi)
				else:
					transProb = term0*Decimal(probj)
			else:
				if j == 0:
					term0 = poissonProb(advLambd,0, t-c*t)
					termNon0 = 1-term0
					nprob1i = nProb(advLambd, lambdi, 2*t-t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t -t)
					transProb = termNon0  + term0*(nprob1i + term01i*Decimal(advProb))
				elif i == j:
					term0 = poissonProb(advLambd,0,t-c*t)
					nprobi1 = nProb(lambdi, advLambd, 2*t-t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t -t)
					transProb = term0*(nprobi1 + term01i*Decimal(probi))
				else:
					term0 = poissonProb(advLambd, 0, t-c*t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t -t)
					transProb = Decimal(probj)*term0*term01i

			skipTranstion[i][j] = transProb

def computeSkipAllTransition(t, gLambd):
	advProb = initProb[0]
	advLambd = advProb*gLambd
	for i in range(0, numNodes):
		probi = initProb[i]
		lambdi = probi*gLambd
		for j in range(0, numNodes):
			transProb = Decimal(0.0)
			probj = initProb[j]
			lambdj = probj*gLambd
			if i == 0:
				term0 = poissonProb(lambdi, 0, 2*t)
				termNon0 = 1-term0
				if i == j:
					transProb = termNon0 + term0*Decimal(probi)
				else:
					transProb = term0*Decimal(probj)
			else:
				if j == 0:
					term0 = poissonProb(advLambd, 0, t)
					termNon0 = 1-term0
					nprob1i = nProb(advLambd, lambdi, 2*t-t)
					term01i = poissonProb(advLambd+lambdi, 0, 2*t-t)
					transProb = termNon0 + term0*(nprob1i + term01i*Decimal(advProb))
				elif i == j:
					term0 = poissonProb(advLambd, 0, t)
					nprobi1 = nProb(lambdi,advLambd, 2*t-t)
					term01i = poissonProb(lambdi+advLambd, 0, 2*t-t)
					transProb = term0*(nprobi1 + term01i*Decimal(probi))
				else:
					term0 = poissonProb(advLambd, 0, t)
					term01i = poissonProb(lambdi+advLambd, 0, 2*t-t)
					transProb = Decimal(probj)*term0*term01i
			skipTranstion[i][j] = transProb

def checkTransitionMatrix(rowCheck, matrix, numRows, th):
	if rowCheck:
		for i in range(0, numRows):
			rowSum = Decimal(0.0)
			for j in range(0, numRows):
				rowSum = rowSum + matrix[i][j]
			if rowSum < th:
				print("Too low rowSum for",i, float(rowSum))
			elif rowSum > -1*th+2:
				print("Too high rowSum for",i, float(rowSum))


def printTransition(matrix):
	for i in range(0,numNodes):
		for j in range(0,numNodes):
			print(round(float(matrix[i][j]),4), end="\t")
		print("\n")
	print("+-------------------------------+")

def printStationary(vector):
	for j in range(0,numNodes):
		print(round(float(vector[j]),4), end=" ")
	print("\n")

initProb = [0.3297630187360915, 0.16161252867434858, 0.15059349262825678, 0.05715206695815737, 0.056711305516792994, 0.04407614418436712, 0.04143157553318527, 0.03526091534709429, 0.026078385308518044, 0.018365060077152478, 0.013421185904173738, 0.013222843254910724, 0.01248824085230392, 0.010504814363667899, 0.008080626433667502, 0.005939260428950312, 0.0015793951668028662, 0.0011019036049087372, 0.0008815228837272837, 0.0008741768594216269, 0.000844792763197531, 0.0008080626436663093, 0.0008080626436663093, 0.0007346024026068043, 0.0007346024026068043, 0.0006244120430146082, 0.0005876819224848558, 0.0005876819224848558, 0.0005771036480039461, 0.00044076144136437643, 0.00036730120130340217, 0.00036730120130340217, 0.00036730120130340217, 0.00035995517799627627, 0.00035995517799627627, 0.0002277267444885795, 0.0001542665044276052, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853]

# initProb = [0.5, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

# initProb = [0.9,0.1]




processTime = [4]
recipLambd = 15.0
numNodes = len(initProb)
checkMatrixTh = 1-10**(-15)
stationaryTh = 10**(-14)

honestTranstion = [[Decimal(0) for x in range(numNodes)] for y in range(numNodes)] 
skipTranstion = [[Decimal(0) for x in range(numNodes)] for y in range(numNodes)] 



honestResults = {}
honestResultsExtended = {}

skipResults = {}
skipResultsExtended = {}


strategy = sys.argv[1]
# processTime = [0.0, 0.2, 0.5, 1, 2, 4]
processTime = [0.16562, 2.4297600000000004, 5.19912]
cList = [0.6]
# interArrivals = [15.33124, 19.85952, 25.39824]



stationaryResults ={}
for t in processTime:
	# globalLambd = 1.0/(recipLambd-2*t)
	globalLambd = 1.0/(recipLambd)
	if strategy == 'adva':
		computeSkipAllTransition(t, globalLambd)
		checkTransitionMatrix(True, skipTranstion, numNodes, checkMatrixTh)
		numitr, probs = computeStationaryProb(skipTranstion, stationaryTh)
		stationaryResults[t] = probs[0]
		print(probs[0])
		continue
	else:
		stationaryResults[t] = {}
		for c in cList:
			if strategy == 'honest':
				if c <= 0.5:
					computeHonestTransitionFast(t, c, globalLambd)
				else:
					computeHonestTransitionSlow(t, c, globalLambd)
				checkTransitionMatrix(True, honestTranstion, numNodes, checkMatrixTh)
				numitr, probs = computeStationaryProb(honestTranstion, stationaryTh)
				stationaryResults[t][c] = probs[0]
				print(probs[0])
			elif strategy == 'advc':
				computeSkipCreateTransition(t, c, globalLambd)
				checkTransitionMatrix(True, skipTranstion, numNodes, checkMatrixTh)
				numitr, probs = computeStationaryProb(skipTranstion, stationaryTh)
				stationaryResults[t][c] = probs[0]
				print(round(probs[0],3))

file = open('/home/sourav/EVD-Expt/data/stat/stat-'+str(strategy)+'.csv', 'a+')
if strategy ==  'adva':
	file.write("t,frac\n")
	for t in processTime:
		file.write(str(t)+","+str(round(stationaryResults[t],3))+"\n")
else:
	file.write("t")
	for c in cList:
		file.write(',c'+str(int(c*100)))
	file.write('\n')
	for t in processTime:
		file.write(str(t))
		for c in cList:
			file.write(","+str(round(stationaryResults[t][c],3)))
		file.write("\n")
