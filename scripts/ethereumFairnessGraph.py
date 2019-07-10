''' 
Note : Here you may have to rename the data folder accordingly 

This script calculates the fraction of blocks mined by miner 
in the main chain and expected number of block mined by 
a miner present in the main chain based on his mining power

ETH-NS-D-HET:
ETH-400-NoSkip-1x-Het

ETH-NS-D-HOMO:
ETH-40-NoSkip-1x-Homo

ETH-NS-ND-HET:
ETH-40-NoSkip-1x-Het  ETH-800-NoSkip-1x-Het

ETH-NS-ND-HOMO:
ETH-40-NoSkip-XX-Homo

ETH-S-ND:
ETH-120-Skip-1x  ETH-12-Skip-1x  ETH-240-Skip-1x

EVD-NS-D:
EVD800_1xDelay  EVD800_2xDelay  EVD800_4xDelay

EVD-NS-ND:
EVD400  EVD-40-NoSkip-XX-Het  EVD800

EVD-S-D:
EVD120_1xDelay_With_Skip  EVD240_1xDelay_With_skip

'''

import time
import numpy as np
import matplotlib.pyplot as plt
import os 


filePath = '/home/sourav/EVD-Segate/'

ethDir = [
	'ETH-NS-D-HET',
	'ETH-NS-D-HOMO',
	'ETH-NS-ND-HET',
	'ETH-NS-ND-HOMO',
	'ETH-S-ND'
]

evdDir = [
	'EVD-NS-D',
	'EVD-NS-ND',
	'EVD-S-D'
]

mainChainBlockList = []
miningInfoList = []
plotMainChainBlockList = []
plotMiningInfoList = []
plotExecutionTime = []
plotExpectedBlocks = []

def computeFairness(inputFilePath, outputFile, startBlk, endBlk):
	
	# 0xdb719d2e7cc1390e46f141a2e4978e9f49f16d63242c5d66f99aa33fef2e5300 15 282 400000000 396576869 0xbd611E337D54dfdbe9A052Fe689a7486cB59156c 664.650ms
	# Extracting the miners who mined at least one block
	addressList = {}
	firstMiner = ""
	for j in range(0,49):
		fileName = inputFilePath+'Mi/'+str(j)+'.dat'

		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			for dataItem in data:
				info = dataItem.split(' ')
				addressList[info[5]] = j
				if j == 0:
					firstMiner = info[5]
				break

	# 14,0x79068e34c77770f599afe5bf18f70326e7c4744b712a28d9ccba282eee91c65c,0xbd611E337D54dfdbe9A052Fe689a7486cB59156c,283,400000000,398949296
	# Compute the number of blocks mined by a miner in 
	miningFrac = {}
	fileName = inputFilePath+'Mc/0.dat'
	if os.path.exists(fileName):
		file = open(fileName, "r")
		data = file.readlines()

		for dataItem in data:
			info = dataItem.split(',')
			blkNum = int(info[0])
			if blkNum < startBlk:
				continue
			elif blkNum > endBlk:
				break
			else:
				miner = info[2]
				if miningFrac.get(miner):
					miningFrac[miner] = miningFrac[miner] + 1
				else:
					miningFrac[miner] = 1

	# 0x8414b5ad8f95e31473f5ab3372729317a07567edd2d9501ad8908105dda110bb 13 0 400000000 0 0x6F75AeB2465dAac2B630667efF18481BE2dEfabd false 0.21846 1.32698
	# Compute the average Execution time:
	avgExTime = {}
	for j in range(0,49):
		fileName = inputFilePath+'Ex/'+str(j)+'.txt'
		if os.path.exists(fileName):
			file = open(fileName, "r")
			data = file.readlines()

			totalExTime = 0.0
			totalProcTime =  0.0
			totalBlks = 0
			for dataItem in data:
				info = dataItem.rstrip().split(' ')
				blkNum = int(info[1])
				if blkNum < startBlk:
					continue
				elif blkNum > endBlk:
					continue
				else:
					totalExTime = totalExTime + float(info[7])
					totalProcTime = totalProcTime + float(info[8])
					totalBlks = totalBlks + 1
			avgExTime[j] = [totalExTime/totalBlks, totalProcTime/totalBlks]
			print(j, totalExTime/totalBlks, totalProcTime/totalBlks, totalBlks)
			

	print(miningFrac[firstMiner])
	print(avgExTime[0])
	print(avgExTime[1])



	# print("*************************************")
	# fileName = filePath+str(gas)+'M/Mi/'+str(0)+".dat"
	# if os.path.exists(fileName):
	# 		file = open(fileName, "r")
	# 		data = file.readlines()

	# 		for dataItem in data:
	# 			info = dataItem.split(' ')
	# 			#print(str(info[0]))
	# 			miningInfoList.append(info[0])

	# count = 0
	# for line in miningInfoList:
	# 	if line in mainChainBlockList:
	# 		count = count+1
	# print(str(count) +" : "+str(len(mainChainBlockList))+" : "+str(0.3302*len(mainChainBlockList)))
	# plotMainChainBlockList.append(len(mainChainBlockList))
	# plotMiningInfoList.append(count)
	# plotExpectedBlocks.append(0.3302*len(mainChainBlockList))

	# toWrite = str(len(mainChainBlockList))+","+str(count)+","+str(0.3302*len(mainChainBlockList))+","

	# fileName = filePath+str(gas)+'M/Ex/'+str(0)+".txt"
	# #print(fileName)
	# count = 0
	# sumExTime = 0
	# avgExTime = 0
	# if os.path.exists(fileName):
	# 		file = open(fileName, "r")
	# 		data = file.readlines()

	# 		for dataItem in data:
	# 			info = dataItem.split(' ')
	# 			#print(info[7])
	# 			sumExTime = sumExTime+float(info[7])
	# 			count = count+1
	# print(str(sumExTime/count))			
	# plotExecutionTime.append(sumExTime/count)
	# print("*************************************")

	# toWrite = toWrite+str(sumExTime/count)+"\n"
	# outputFile.write(toWrite)
					

	# mainChainBlockList.clear()
	# miningInfoList.clear()
	# /home/sourav/EVD-Segate/ETH-S-ND/ETH-12-Skip-1x/Mi

def computeEthSkip():
	dirPath = '/home/sourav/EVD-Segate/ETH-S-ND/'
	gasList = [12, 120, 240]
	fileNames =[
		'ETH-12-Skip-1x/',
		'ETH-120-Skip-1x/',
		'ETH-240-Skip-1x/'
	]

	outputFilePath = '/home/sourav/EVD-Expt/data/skipFract.csv'
	outputFile = open(outputFilePath,"w+")
	outputFile.write("totalBlocks,minerBlocks,expBlocks,avgExecTime\n")
	    
	for i in range(0,3):
		inputFilePath =  dirPath+fileNames[i]
		computeFairness(inputFilePath, outputFile, 25, 1025)

hashFilePath = '/home/EV'
hashPowers = readHashPower()
computeEthSkip()