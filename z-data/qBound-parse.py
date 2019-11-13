'''
This file parses the data and writes them
into appropriate .csv file
'''

import os
import matplotlib.pyplot as plt

advFracs = [10,25,33]
procs = [15,30,50,75]
advFracs = [25,33]
procs = [30,50]
cvals  = [x for x in range(100,1,-5)]
errorTh = 0.01

def parseFile(fileName):
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()
		zetaValues = []
		i = 0
		for dataItem in data:
			info = dataItem.split(" ")
			if info[0] == 'c':
				cVal = info[-1]
				zetaLine = (data[i-2]).split(" ")
				zeta = zetaLine[0]
				zetaValues.append(zeta)
			i=i+1
		return zetaValues
	else:
		print(fileName," file not found!!")



dirPath =  os.environ["HOME"]+"/EVD-Expt/z-data/"

resultData = {}
for adv in advFracs:
	resultData[adv] = {}
	for proc in procs:
		fileName = dirPath+"z-0"+str(1)+"-"+str(adv)+"-"+str(proc)
		zetaValues = parseFile(fileName)
		resultData[adv][proc] = zetaValues
	print(resultData[adv])

advFracs = [25,33]
procs = [30,50]

plt.figure(1)
for adv in advFracs:
	for proc in procs:
		plt.plot(cvals,resultData[adv][proc] , label="f="+str(adv)+",tau/intv="+str(round(proc*1.0/150,2)))
	#plt.plot(blockNumberList,gasUsageListTotal , label='Gas used')
plt.grid(True)
plt.legend(loc="upper right")

plt.xlabel('c')
plt.ylabel('zeta')
plt.title('zeta required to bound the fraction of time queue overflows')
plt.show()
