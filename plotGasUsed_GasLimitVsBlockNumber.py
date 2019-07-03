'''This script calculate the variation in block gas limit and block gas used  with blockNumber, here we are planning to answer how well user can predict the gas uses'''


import time
import numpy as np
import matplotlib.pyplot as plt

filePath = '/home/nitin14/EVD-Scripts/TxGasUsage/'

blockNumberList = []
totalTxnList = []
paymentTxnList = []
gasUsageList = []
gasLimitList = []
gasLimitListTotal=[]
gasUsageListTotal=[]
gasUsedFraction=[]
def computeGasLimit(interval):
	
	
	fileName = ""
	outputFilePath = '/home/nitin14/EVD-Scripts/gasUsedGasLimitFract.csv'
	outputFile = open(outputFilePath, "w+")
	outputFile.write("blockHeight,gasLimit,gasUsed\n")




	currentBlock = 0
	txCount = 1
	paymentCount = 0
	blkGasUsed = 0
	blkGasLimit = 0

	for i in range(0,56):
		
		fileName = filePath+'gasLimitGasUsed_'+str(i)+".txt"
		file = open(fileName, "r")
		data = file.readlines()

		j=1
		txnCountList = np.zeros(interval)
		paymentCountList = np.zeros(interval)
		gasUsedList = np.zeros(interval)
		gasLimitList = np.zeros(interval)

		for dataItem in data:
			info = dataItem.split(', ')

			blkNumber = int(info[0])
			if blkNumber != currentBlock:

				txnCountList[currentBlock%interval] = txCount
				paymentCountList[currentBlock%interval] = paymentCount
				gasUsedList[currentBlock%interval] = blkGasUsed/txCount
				gasLimitList[currentBlock%interval] = blkGasLimit/txCount

				j = j+1

				if j%interval == 0:
					avgTxnCount =  np.mean(txnCountList)
					avgPaymentCount = np.mean(paymentCountList)
					avgGasUsed  = np.mean(gasUsedList)
					avgGasLimit  = np.mean(gasLimitList)
					avgblkNumber = currentBlock - interval/2

					blockNumberList.append(blkNumber)
					totalTxnList.append(avgTxnCount)
					paymentTxnList.append(avgPaymentCount)
					gasUsageListTotal.append(avgGasUsed)
					gasLimitListTotal.append(avgGasLimit)
					gasUsedFraction.append(avgGasUsed/avgGasLimit)

					toWrite = str(avgblkNumber)+","+str(avgGasUsed)+","+str(avgGasLimit)+","+str(avgGasUsed/avgGasLimit)+"\n"
					outputFile.write(toWrite)

					txnCountList = np.zeros(interval)
					paymentCountList = np.zeros(interval)
					gasUsedList = np.zeros(interval)
					gasLimitList = np.zeros(interval)

				currentBlock = blkNumber
				txCount = 0
				paymentCount = 0
				blkGasUsed = 0
				blkGasLimit = 0

			gasLimit = float(info[2])
			gasUsed = float(info[3])

			txCount = txCount+1
			blkGasUsed = blkGasUsed + gasUsed
			blkGasLimit = blkGasLimit+gasLimit

			if gasUsed == 21000:
				paymentCount = paymentCount+1

	outputFile.close()
	print(len(blockNumberList))
	print("*****************************************************")
	print(len(gasUsageListTotal))


	plt.figure(1)
	#plt.plot(blockNumberList,gasLimitListTotal , label='Gas limit')
	#plt.plot(blockNumberList,gasUsageListTotal , label='Gas used')
	plt.plot(blockNumberList,gasUsedFraction , label='ratio of gasUsed to gasLimit')

	plt.grid(True)
	plt.legend(loc="upper left")

	plt.xlabel('Block height')
	plt.ylabel('Gas')
	plt.title('Gas usage and limit with increasing block height')
	plt.show()

computeGasLimit(10000)