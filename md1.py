import sys
import math 
import numpy as np
import matplotlib.pyplot as plt

from decimal import *
getcontext().prec = 300

'''
Results from Previous Runs

1. 5x Scalability
+-----------+----------+
|	32		|	  5    |
|	40		|	  7    |
|	48		|	  8    |
|	56		|	  10   |
|	64		|	  11   |
|	72		|	  13   |
|	80		|	  15   |
|	88		|	  16   |
|	96		|	  18   |
|	104		|	  19   |
|	112		|	  21   |
|	120		|	  22   |
|	128		|	  24   |
+-----------+----------+

2. 10x Scalability
+-----------+----------+
|	32		|	  8    |
|	40		|	  10   |
|	48		|	  12   |
|	56		|	  14   |
|	64		|	  16   |
|	72		|	  18   |
|	80		|	  20   |
|	88		|	  22   |
|	96		|	  24   |
|	104		|	  26   |
|	112		|	  28   |
|	120		|	  30   |
|	128		|	  33   |
+-----------+----------+

3. 20x Scalability
+-----------+----------+
|	32		|	  13   |
|	40		|	  16   |
|	48		|	  20   |
|	56		|	  23   |
|	64		|	  27   |
|	72		|	  30   |
|	80		|	  33   |
|	88		|	  37   |
|	96		|	  40   |
|	104		|	  44   |
|	112		|	  47   |
|	120		|	  51   |
|	128		|	  54   |
+-----------+----------+

'''


def computeProb(lambd, MAX):
	probs = []
	ks.append(0)
	probs.append(Decimal(1)-lambd)
	ks.append(1)
	probs.append((Decimal(1)-lambd)*(np.exp(lambd)-Decimal(1)))

	totalProb = probs[0] + probs[1]

	for i in range(2, MAX):
		term1 = (Decimal(1)-lambd)
		term2 = np.exp(Decimal(i)*lambd)
		
		term3 = Decimal(0.0)
		for j in range(1,i):
			term4 = np.exp(Decimal(j)*lambd)
			term5 = np.power(-1,(Decimal(i)-Decimal(j)))
			term6 = np.power(Decimal(j)*lambd, Decimal(i)-Decimal(j))/(math.factorial(Decimal(i)-Decimal(j)))
			term7 = np.power(Decimal(j)*lambd, Decimal(i)-Decimal(j+1))/(math.factorial(Decimal(i)-Decimal(j+1)))
			term8 = term4*term5*(term6 + term7)
			term3 = term3 + term8

		result = term1*(term2 + term3)
		if result < Decimal(0):
			print("NEGATIVEEEEEEEEEEEEEEEEEEEEEEEE")
		ks.append(i)
		probs.append(math.log2(result))
		# totalProb = totalProb + result
	# print(i,result)
	return(probs)
# print(totalProb)

def computeK(lambd, MAX, threshold):
	errorProb = Decimal(0)
	i = MAX
	while i > 1:
		term1 = (Decimal(1)-lambd)
		term2 = np.exp(Decimal(i)*lambd)
		
		term3 = Decimal(0.0)
		for j in range(1,i):
			term4 = np.exp(Decimal(j)*lambd)
			term5 = np.power(-1,(Decimal(i)-Decimal(j)))
			term6 = np.power(Decimal(j)*lambd, Decimal(i)-Decimal(j))/(math.factorial(Decimal(i)-Decimal(j)))
			term7 = np.power(Decimal(j)*lambd, Decimal(i)-Decimal(j+1))/(math.factorial(Decimal(i)-Decimal(j+1)))
			term8 = term4*term5*(term6 + term7)
			term3 = term3 + term8

		result = term1*(term2 + term3)
		if result < Decimal(0):
			print("NEGATIVEEEEEEEEEEEEEEEEEEEEEEEE")
		errorProb = errorProb + result
		if errorProb > threshold:
			return (i-1)
		i=i-1

	errorProb = errorProb + (Decimal(1)-lambd)*(np.exp(lambd)-Decimal(1))
	if errorProb > threshold:
		return 1

	errorProb = errorProb + (Decimal(1)-lambd)
	if errorProb > threshold:
		return 0
	return None


MAX = 100 + 1
# lambd = Decimal(1)/Decimal(15.0)
lambdA = Decimal(1)/Decimal(15.0) + Decimal(1)/Decimal(30)
# ks = []
# probHonest = computeProb(lambd, MAX)
# ks = []
# probAdv = computeProb(lambdA, MAX)

kValues = []
betaValues = []
beta = 32
while beta <= 128:
	kValue = computeK(lambdA, MAX, math.pow(2,-1*beta))
	if kValue is None:
		beta = beta + 8
		print("None k Values")
		continue
	kValues.append(kValue)
	betaValues.append(beta)
	print(beta,",",kValue)
	beta = beta+8



kValues2 = []
lambd2 = Decimal(1)/Decimal(5.0)
beta = 32
while beta <= 128:
	kValue = computeK(lambd2, MAX, math.pow(2,-1*beta))
	if kValue is None:
		beta = beta + 8
		print("None k Values")
		continue
	kValues2.append(kValue)
	print(beta,",",kValue)
	beta = beta+8

kValues4 = []
lambd4 = Decimal(1)/Decimal(2.5)
beta = 32
while beta <= 128:
	kValue = computeK(lambd4, MAX, math.pow(2,-1*beta))
	if kValue is None:
		beta = beta + 8
		print("None k Values")
		continue
	kValues4.append(kValue)
	print(beta,",",kValue)
	beta = beta+8


plt.figure(1)
# plt.plot(ks, probHonest, label='Probability')
# plt.plot(ks, probAdv, label='Probability with Adv')
plt.plot(betaValues, kValues, label='5x Ethereum Gas Limit')
plt.plot(betaValues, kValues2, label='10x Ethereum Gas Limit')
plt.plot(betaValues, kValues4, label='20x Ethereum Gas Limit')
plt.grid(True)
plt.legend(loc="upper left")

plt.xlabel('-ve of Log2 (Probability (Q>k))')
plt.ylabel('Required k')
# plt.title('Gas usage and limit with increasing block height')
plt.show()
