'''
This file computes the general upper bound on the 
probability that queue of an honest miner will exceed
zeta for a given value of zeta.

Manually written functions for Bessel and Skellam are in misc.py

This file contains multiple components.
	1. Compute Delta for a given c
	2. Use Delta to compute bwTime (block withholding) time
	3. Use bwTime, Delta to compute the upper bound queue exceeding zeta probability.
	4. Plot the results

'''

import sys
import numpy as np
import math
from scipy.stats import skellam

from decimal import *
getcontext().prec = 400


def computeDelta(c, gLambd):
	return Decimal(1.0)/(gLambd*c)

def abs(x):
	if x<0:
		return (-1)*x
	return x
	

def computeSkellam(meanH, meanA):
	return Decimal(1.0)-Decimal(skellam.cdf(0, float(meanH), float(meanA), loc=0))
	

'''
Perform a binary search over time to find the minimum 
time for which the required bound holds
'''
def computeBwTime(delta, bwTh, advFrac):
	tMin = 1
	tMax = 1000 # in multiples of delta advFrac*tMax/c expected number of adversarial blocks 
	tCurr = (tMin+tMax)/2
	hstDiscount = Decimal(math.exp(Decimal(-1*(1-advFrac)*gLambd)*delta))
	while (tMax-tMin)>2:
		meanH = Decimal(tCurr)*(hstDiscount*Decimal(1-advFrac)*gLambd)
		meanA = Decimal(tCurr)*(Decimal(advFrac)*gLambd)
		sProb = computeSkellam(meanH, meanA)
		if (sProb <= 1-bwTh):
			tMin = tCurr
			tCurr = (tMin+tMax)/2
		else:
			tMax = tCurr
			tCurr = (tMin+tMax)/2
	# print("tMin:", tMin,"tMax:", tMax, "tCurr:", tCurr, "sProb: ", round(sProb,10))
	return tCurr

def computeEpsilon(interval, delay):
	return Decimal(delay)/Decimal(interval)		# we want: s+delta >= (1+epsilon)*s

# To stationary probability of given queue length
def computeProb(lambd, qSize):
	term1 = (Decimal(1)-lambd)
	term2 = np.exp(Decimal(qSize)*lambd)
	
	term3 = Decimal(0.0)
	for j in range(1,qSize):
		term4 = np.exp(Decimal(j)*lambd)
		term5 = np.power(-1,(Decimal(qSize)-Decimal(j)))
		term6 = np.power(Decimal(j)*lambd, Decimal(qSize)-Decimal(j))/(math.factorial(Decimal(qSize)-Decimal(j)))
		term7 = np.power(Decimal(j)*lambd, Decimal(qSize)-Decimal(j+1))/(math.factorial(Decimal(qSize)-Decimal(j+1)))
		term8 = term4*term5*(term6 + term7)
		term3 = term3 + term8

	result = term1*(term2 + term3)
	return result

# This is computing tail probability of a given z
def computeMd1Tail(lambd, z, md1Th):
	qSize = z
	tailProb = 0
	while True:
		termProb = computeProb(lambd, qSize)
		tailProb = tailProb + termProb
		if termProb < md1Th:
			break
		qSize = qSize + 1
	return tailProb

def poissonProb(lambd, k, t):
	nTerm1 = Decimal(math.pow(Decimal(lambd*t), Decimal(k)))
	nTerm2 = Decimal(np.exp(-1*(lambd*t)))
	dTerm1 = Decimal(math.factorial(k))

	return nTerm1*nTerm2/dTerm1

def computPoissonHead(lambd, s, zeta):
	totalProb = 0
	for i in range(0,zeta+1):
		termProb = poissonProb(lambd,i, s)
		totalProb = totalProb + termProb
	return totalProb

def computeS0(delta, eH, bwTime, eA):
	if Decimal(delta)/Decimal(eH) > Decimal(bwTime)/Decimal(eA):
		return Decimal(delta)/Decimal(eH)
	return Decimal(bwTime)/Decimal(eA)

def printRounded(pc):
	print("c 		:"+str(round(c,pc)))
	# print("advFrac 	:"+str(round(advFrac,pc)))
	print("gLambd 	:"+str(round(gLambd,pc)))
	print("delta	:"+str(round(delta,pc)))
	print("bwTime 	:"+str(round(bwTime,pc)))
	print("epsilonH :"+str(round(epsilonH,pc)))
	print("epsilonA :"+str(round(epsilonA,pc)))
	print("eLambd 	:"+str(round(lambd,pc)), round(1/lambd,pc))
	print("s0 		:"+str(round(s0,pc)))
	print("md1Tail 	:"+str(round(md1Tail,pc)))
	print("pTail 	:"+str(round(poissonTail,pc)))
	print("prob 	:"+str(round(prob,pc)))

def printRaw():
	pc = 400
	print("c 		:"+str(round(c,pc)))
	print("advFrac 	:"+str(round(advFrac,pc)))
	print("gLambd 	:"+str(round(gLambd,pc)))
	print("delta	:"+str(round(delta,pc)))
	print("bwTime 	:"+str(round(bwTime,pc)))
	print("eH 		:"+str(round(epsilonH,pc)))
	print("eA 		:"+str(round(epsilonA,pc)))
	print("eLambd 	:"+str(round(lambd,pc)))
	print("s0 		:"+str(round(s0,pc)))
	print("md1Tail 	:"+str(round(md1Tail,pc)))
	print("pTail 	:"+str(round(poissonTail,pc)))
	print("prob 	:"+str(round(prob,pc)))


gLambd = Decimal(1/15.0)
advFrac = Decimal(0.25)
bwTh = Decimal(math.pow(2,-10))

# We want to find the value of minimum zeta, such that the required bound holds
z = 30
tau = Decimal(5.0) # Say it takes 1/4th of average interarrival time to process a block.

sList = [x for x in range(100,1000,100)]
# c is essentially number expected time in delta as the unit of time 
for s1 in sList:
	s = Decimal(s1)
	for c in range(7,11,5):
		delta = computeDelta(c,gLambd)
		bwTime = computeBwTime(delta, bwTh, advFrac)
		epsilonH = computeEpsilon(s, delta)
		epsilonA = computeEpsilon(s, bwTime)
		lambd = (1+epsilonH)*(1-advFrac)*gLambd + (1+epsilonA)*advFrac*gLambd
		s0 = computeS0(delta, epsilonH, bwTime, epsilonA)
		md1Tail = computeMd1Tail(tau*lambd, z, math.pow(2,-30)) 
		poissonTail = 1-computPoissonHead(lambd, s0, z)
		prob = md1Tail+poissonTail
		# printRounded(15)
		print(s1,round(prob,10))
		print("---------")







