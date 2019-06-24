import time
import numpy as np
import matplotlib.pyplot as plt

filePath = '/ssd/data/'

blockNumberList = []
totalTxnList = []
paymentTxnList = []
gasUsageList = []
gasLimitList = []
gasLimitListTotal=[]
gasUsageListTotal=[]
def computeGasLimit(interval):
	
	
	fileName = ""
	outputFilePath = '/home/sourav/EVD-Expt/paymentTxnMeasurement.csv'
	outputFile = open(outputFilePath, "w+")
	outputFile.write("blockHeight,gasLimit,gasUsed\n")


	currentBlock = 0
	txCount = 1
	paymentCount = 0
	blkGasUsed = 0
	blkGasLimit = 0
	glTxMap = {}


	for i in range(7700001,7700002):
		
		fileName = filePath+'gasLimitGasUsed_'+str(i)+".txt"
		file = open(fileName, "r")
		data = file.readlines()


		for dataItem in data:
			info = dataItem.split(', ')

			'''
					toWrite = str(avgblkNumber)+","+str(avgGasUsed)+","+str(avgGasLimit)+"\n"
					outputFile.write(toWrite)
			'''

			gasLimit = float(info[2])
			gasUsed = float(info[3])
			if gasUsed == 21000:
				continue;
			if int(gasLimit/10) not in glTxMap:
				txList = []
				txFrequenceyList = []
				txList.append(0)
				for j in range(0,101):
					txFrequenceyList.append(0)
				txList.append(txFrequenceyList)
				glTxMap[int(gasLimit/10)] = txList

			glTxMap[int(gasLimit/10)][0] += 1
			#print(int(round(gasUsed/gasLimit , 2)*100))
			glTxMap[int(gasLimit/10)][1][int(round(gasUsed/gasLimit , 2)*100)] += 1	
			txCount = txCount+1

	cumulativeList = []
	gasFract = []
	for j in range(0,101):
		cumulativeList.append(0)
		gasFract.append(j/100)

	for key,value in glTxMap.items():
		#cumulativeList.append()
		cumulativeList = [cumulativeList[j] + value[1][j] for j in range(len(value[1]))] 
		print(str(key) + " ::::::: ", end = '')
		print(value[1])
	
	print(cumulativeList)
	for j in range(0,101):
		cumulativeList[j] = cumulativeList[j]/txCount

	print("*****************************************************")

	print(cumulativeList)
	outputFile.close()
	#print(cumulativeList)
	
	#print(len(gasUsageListTotal))


	plt.figure(1)
	plt.plot(gasFract,cumulativeList , label='Gas limit')
	#plt.plot(blockNumberList,gasUsageListTotal , label='Gas used')
	plt.grid(True)
	plt.legend(loc="upper left")

	plt.xlabel('Block height')
	plt.ylabel('Gas')
	plt.title('Gas usage and limit with increasing block height')
	plt.show()

computeGasLimit(1000)