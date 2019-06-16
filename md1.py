import sys
import math 
import numpy as np
import matplotlib.pyplot as plt

from decimal import *
getcontext().prec = 300


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


MAX = 100 + 1
lambd = Decimal(1)/Decimal(15.0)
lambdA = Decimal(1)/Decimal(15.0) + Decimal(1)/Decimal(7.5)
ks = []
probHonest = computeProb(lambd, MAX)
ks = []
probAdv = computeProb(lambdA, MAX)

plt.figure(1)
plt.plot(ks, probHonest, label='Probability')
plt.plot(ks, probAdv, label='Probability with Adv')
plt.grid(True)
plt.legend(loc="upper left")

plt.xlabel('Queue size')
plt.ylabel('Probability')
# plt.title('Gas usage and limit with increasing block height')
plt.show()
