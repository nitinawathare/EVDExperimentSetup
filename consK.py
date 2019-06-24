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

def sumPoissonProb(lambd, lowerK, t, threshold):
	index = lowerK
	totalProb = Decimal(0.0)
	while True:
		prob = poissonProb(lambd, index, t)
		if prob < threshold:
			break
		totalProb = totalProb + prob
		index = index + 1
	return totalProb

def computeSuccess(lambd, maxK, t, th):
	
	successProb = np.zeros((maxK,maxK))

	# All probabilities above the line x=y will be 1
	for i in range(1, maxK):
		for j in range(i, maxK):
			successProb[i][j] = Decimal(1.0)

	for i in range(1, maxK):
		for j in range(1,i):
			prob = Decimal(0.0)
			for k in range(1, i-j+1):
				term1 = Decimal(poissonProb(lambd, k, (j+1)*t))
				term2 = Decimal(successProb[i-j][k])
				prob = Decimal(prob + term1*term2)
			prob = Decimal(prob) + Decimal(sumPoissonProb(lambd, i-j+1, (j+1)*t, th))
			successProb[i][j] = Decimal(prob)
			# print(j,i, round(prob, 10))

	totalProb = Decimal(0.0)
	for j in range(1, maxK):
		term1 = Decimal(math.pow(Decimal(1.0/3.0), j))
		totalProb = totalProb + term1*Decimal(successProb[maxK-1][j])
	return totalProb

# success0 = Decimal(math.pow(Decimal(1.0/3.0), 5))
# success4s = computeSuccess(1.0/30.0, 6, 4, math.pow(2, -64))
# success200ms = computeSuccess(1.0/30.0, 6, 0.2, math.pow(2, -64))

# print("Success with zero delay:", success0)
# print("Success with 200 milliseconds:", success200ms, "ratio: ", success200ms/success0)
# print("Success with 4 seconds:", success4s, "ratio: ", success4s/success0)


processTime = {'200ms':0.2, '500ms':0.5, '1s':1, '2s':2, '4s':4}

lValues = []
results = {}
zeroProcessTime = []
threshold = math.pow(2, -64)

MAX_L = 28

ofile = open("/home/sourav/EVD-Expt/consL.csv","w+")
ofile.write("lValue,zero,t200ms,t500ms,t1s,t2s,t4s\n")

for l in range(2,MAX_L):
	zeroTime = math.log2(Decimal(math.pow(Decimal(1.0/3.0), l)))
	zeroProcessTime.append(zeroTime)
	lValues.append(l)

	ofile.write(str(l))
	ofile.write(","+str(zeroTime))
	
	for k, value in processTime.items():
		prob = computeSuccess(1.0/30.0, l+1, value, threshold)
		if k not in results:
			results[k] = [math.log2(prob)]
		else:
			results[k].append(math.log2(prob))

		ofile.write(","+str(math.log2(prob)))
	ofile.write("\n")

ofile.close()
	
# plt.figure(1)

# plt.plot(lValues, zeroProcessTime, label='0 seconds')
# plt.plot(lValues, results['200ms'], label='200 ms')
# plt.plot(lValues, results['500ms'], label='500 ms')
# plt.plot(lValues, results['1s'], label='1 s')
# plt.plot(lValues, results['2s'], label='2 s')
# plt.plot(lValues, results['4s'], label='4 s')

# plt.grid(True)
# plt.legend(loc="upper right")
# plt.xlabel('Number of consecutive blocks')
# plt.ylabel('Success probability (log base 2)')
# plt.show()

