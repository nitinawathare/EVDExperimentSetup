'''

This graph computes the increase in probability
of mining the 2nd block from the current block
height in the presence of an:
	i)	Honest miner
	ii)	Adversary that skips validation

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

	return float(nTerm1*nTerm2/dTerm1)

def computeHonestFinalProb(index, t, gLambd):
	myProb = initProb[index]
	finalProb = 0.0
	numNodes = len(initProb)
	for i in range(0, numNodes):
		prob = initProb[i]
		if i == index:
			term0 = poissonProb(gLambd*prob, 0, t)
			termNon0 = 1-term0
			term1 = term0*myProb
			finalProb = finalProb + prob*(termNon0 + term1)	
		else:
			term0 = poissonProb(gLambd*prob, 0, t)
			term2 = term0*myProb
			finalProb = finalProb + prob*term2
	return finalProb

def computeSkipFinalProb(index, t, gLambd):
	myProb = initProb[index]
	advProb = initProb[0]
	
	finalProb = 0.0
	numNodes = len(initProb)
	for i in range(0, numNodes):
		prob = initProb[i]
		if index == 0: # Computing adversary's success probability
			if i == index:
				term0 = poissonProb(gLambd*prob, 0, t)
				termNon0 = 1-term0
				term1 = term0*myProb
				finalProb = finalProb + prob*(termNon0 + term1)
			else:
				term0 = poissonProb(gLambd*(myProb + prob), 0, t)
				termNon0 = 1-term0
				term1 = term0*myProb
				term2 = termNon0*(myProb/(myProb+prob))
				finalProb = finalProb + prob*(term1 + term2)

		else:
			if index == i:
				term0 = poissonProb(gLambd*(myProb + advProb), 0, t)
				termNon0 = 1-term0
				term1 = term0*myProb
				term2 = termNon0*(myProb/(myProb+advProb))
				finalProb = finalProb + prob*(term1 + term2)
			elif i == 0:
				term0 = poissonProb(gLambd*prob, 0, t)
				finalProb = finalProb + prob*(term0*myProb)
			else:
				term0 = poissonProb(gLambd*(advProb+prob), 0, t)
				finalProb = finalProb + prob*(term0*myProb)

	return finalProb

initProb = [0.3297630187360915, 0.16161252867434858, 0.15059349262825678, 0.05715206695815737, 0.056711305516792994, 0.04407614418436712, 0.04143157553318527, 0.03526091534709429, 0.026078385308518044, 0.018365060077152478, 0.013421185904173738, 0.013222843254910724, 0.01248824085230392, 0.010504814363667899, 0.008080626433667502, 0.005939260428950312, 0.0015793951668028662, 0.0011019036049087372, 0.0008815228837272837, 0.0008741768594216269, 0.000844792763197531, 0.0008080626436663093, 0.0008080626436663093, 0.0007346024026068043, 0.0007346024026068043, 0.0006244120430146082, 0.0005876819224848558, 0.0005876819224848558, 0.0005771036480039461, 0.00044076144136437643, 0.00036730120130340217, 0.00036730120130340217, 0.00036730120130340217, 0.00035995517799627627, 0.00035995517799627627, 0.0002277267444885795, 0.0001542665044276052, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853, 0.00014692048012194853]

# processTime = [0.0, 0.2, 0.5, 1, 2, 4]
processTime = [0.4]
globalLambd = 1/15.0
results = {}
relativeResults = {}
numNodes = 50

for t in processTime:
	for j in range(0,50 ):
		results[t]=[]
		relativeResults[t]=[]
		for i in range(0, numNodes):
			finalProb = computeHonestFinalProb(i, t, globalLambd)
			results[t].append(finalProb)
			# relativeChange = (finalProb-initProb[i])/initProb[i]
			# relativeResults[t].append(relativeChange)
		initProb = results[t]	
	print(t,"\t\t", sum(results[t]),"\t\t", results[t],"\n\n")
	# print(t,"\t\t", relativeResults[t],"\n\n")

