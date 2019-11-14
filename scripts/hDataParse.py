'''
To parse h-data files
'''

import os
import matplotlib.pyplot as plt

advFracs = [0.25,0.33]
procs = [5.0,7.5]
zValues = [10, 15, 20]
cvals  = [x for x in range(100,1,-5)]

def parseFileZ(fileName, resultData):
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			info = dataItem.split(" ")
			advFrac = float(info[0])
			tau = float(info[1])
			zList = info[2].split(",")
			zDict = {}
			for zItem in zList:
				content = zItem.split(":")
				key = int(content[0])
				value = float(content[1])
				zDict[key]=value
			
			if advFrac not in resultData:
				resultData[advFrac] = {}
			resultData[advFrac][tau]=zDict
	else:
		print(fileName," file not found!!")

def parseFileH(fileName, resultData):
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			info = dataItem.split(" ")
			tau = float(info[0])
			zeta = int(info[1])
			probList = info[2].split(",")
			probs = {}
			for prob in probList:
				content = prob.split(":")
				key = int(content[0])
				value = float(content[1])
				probs[key]=value

			if tau not in resultData:
				resultData[tau]={}
			print(tau,zeta)
			resultData[tau][zeta] = probs
	else:
		print(fileName," file not found!!")


fileName = os.environ["HOME"]+"/EVD-Expt/scripts/z-data-min"
resultDataZ = {}
filez = open("z-data.csv", "w+")
filez.write("c,25-50,25-75,33-50,33-75\n")

parseFileZ(fileName, resultDataZ)
for c in cvals:
	filez.write(str(c))
	for tau in procs:
		for adv in advFracs:
			if c not in resultDataZ[adv][tau]:
				filez.write(",")
			else:
				filez.write(","+str(resultDataZ[adv][tau][c]))
	filez.write("\n")
exit()

dirPath = os.environ["HOME"]+"/EVD-Expt/scripts/"
fileNames = ['h-data']
resultDataH = {}
for file in fileNames:
	filePath = dirPath+file
	parseFileH(filePath, resultDataH)

file = open("h-data.csv", "w+")
file.write("c,10-75,15-75,20-75\n")
proc = 7.5 

for c in cvals:
	file.write(str(c))
	for z in zValues:
		file.write(","+str(resultDataH[proc][z][c]))
	file.write("\n")

