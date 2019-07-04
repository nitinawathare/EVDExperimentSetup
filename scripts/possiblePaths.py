'''

This file computes the probability
in the 2D random walk.

'''

import numpy as np
import math

def numberOfpaths(rows, columns, k):
	honest = 0.67
	adv = 1 - honest
	count = np.zeros((rows,columns))

	for i in range(0, rows):
		count[i][0] = 1

	for j in range(0, columns):
		count[0][j] = 1 

	totalProbablity = 0.0
	totalProbablity = totalProbablity + count[k+1][0]*math.pow(honest, 0)*math.pow(adv, k+1)
	print(0, k+1, count[k+1][0]*math.pow(honest, 0)*math.pow(adv, k+1))

	for i in range(1, columns):
		for j in range(1, rows):

			if (i>k+1 and j<=k) or (i>j+1 and j>k):
				count[i][j] = 0

			if (i==k+1 and j<=k) or (i>=k+1 and (i==j or i==j+1)):
				count[i][j] = count[i-1][j]

			# to only sum the probability terms
			if(i==k+1 and j<=k) or (i>=k+1 and i==j+1):
				totalProbablity = totalProbablity + count[i][j]*math.pow(honest, j)*math.pow(adv, i)
				print(j,i,count[i][j], count[i][j]*math.pow(honest, j)*math.pow(adv, i))

			if (i<=k) or (i>k and i<j):
				count[i][j] = count[i-1][j] + count[i][j-1]

	print(totalProbablity)

numberOfpaths(100,100,100)