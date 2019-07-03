'''This scripts calculate the expected time saved with validation in EVD compared to the one required in ethereum'''


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
contractTransactionList=[]
evdGasUsedList=[]
avgEvdGasUsedList=[]

def computeGasLimit(interval):
	
	
	fileName = ""
	outputFilePath = '/home/nitin14/EVD-Scripts/percentOfContractTransFract.csv'
	outputFile = open(outputFilePath, "w+")
	outputFile.write("blockHeight,gasUsedEthereum,gasUsedEVD\n")


	currentBlock = 0
	txCount = 1
	paymentCount = 0
	blkGasUsed = 0
	blkGasLimit = 0
	contractTxCount = 0

	j=1
	txnCountList = np.zeros(interval)
	paymentCountList = np.zeros(interval)
	gasUsedList = np.zeros(interval)
	gasLimitList = np.zeros(interval)
	contractTransactionList = np.zeros(interval)

	for i in range(50,53):
		
		fileName = filePath+'gasLimitGasUsed_'+str(i)+".txt"
		file = open(fileName, "r")
		data = file.readlines()


		#avgEvdGasUsedList  = np.zeros(interval)
		evdGasUsedList  = np.zeros(interval)
		for dataItem in data:
			info = dataItem.split(', ')

			blkNumber = int(info[0])
			if blkNumber != currentBlock:

				txnCountList[currentBlock%interval] = txCount
				paymentCountList[currentBlock%interval] = paymentCount
				contractTransactionList[currentBlock%interval] = contractTxCount
				evdGasUsedList[currentBlock%interval] = 21000*paymentCount+2*21000*contractTxCount

				#print(str(txCount)+" "+str(paymentCount)+" "+str(contractTxCount))
				gasUsedList[currentBlock%interval] = blkGasUsed#/txCount
				gasLimitList[currentBlock%interval] = blkGasLimit/txCount

				j = j+1

				if j%interval == 0:
					avgTxnCount =  np.mean(txnCountList)
					avgPaymentCount = np.mean(paymentCountList)
					avgGasUsed  = np.mean(gasUsedList)
					avgGasLimit  = np.mean(gasLimitList)
					avgblkNumber = currentBlock - interval/2
					avgEvdGasUsed = 21000*avgPaymentCount+2*21000*(avgTxnCount-avgPaymentCount)#np.mean(evdGasUsedList)

					blockNumberList.append(blkNumber)
					totalTxnList.append(avgTxnCount)
					paymentTxnList.append(avgPaymentCount)
					gasUsageListTotal.append(avgGasUsed)
					gasLimitListTotal.append(avgGasLimit)
					avgEvdGasUsedList.append(avgEvdGasUsed)

					toWrite = str(avgblkNumber)+","+str(avgGasUsed)+","+str(avgEvdGasUsed)+","+str(avgTxnCount)+","+str(avgPaymentCount)+","+str(avgPaymentCount/avgTxnCount)+"\n"
					outputFile.write(toWrite)

					txnCountList = np.zeros(interval)
					paymentCountList = np.zeros(interval)
					gasUsedList = np.zeros(interval)
					gasLimitList = np.zeros(interval)
					evdGasUsedList = np.zeros(interval)
					contractTransactionList= np.zeros(interval)

				currentBlock = blkNumber
				txCount = 0
				paymentCount = 0
				blkGasUsed = 0
				blkGasLimit = 0
				contractTxCount = 0

			gasLimit = float(info[2])
			gasUsed = float(info[3])

			txCount = txCount+1
			blkGasUsed = blkGasUsed + gasUsed
			blkGasLimit = blkGasLimit+gasLimit

			if gasUsed == 21000:
				paymentCount = paymentCount+1
			else :
				contractTxCount = contractTxCount+1


	outputFile.close()
	print(avgEvdGasUsedList)
	print("*****************************************************")
	print(gasUsageListTotal)


	plt.figure(1)
	plt.plot(blockNumberList,avgEvdGasUsedList , label='Gas EVD')
	plt.plot(blockNumberList,gasUsageListTotal , label='Gas used')
	plt.grid(True)
	plt.legend(loc="upper left")

	plt.xlabel('Block height')
	plt.ylabel('Gas')
	plt.title('Gas usage and limit with increasing block height')
	plt.show()

computeGasLimit(10000)