'''

This file is the discrete event simulator 
for adversarial strategy reset.

'''
import sys
import time
import math 
import numpy as np
import os
import heapq
import copy

from decimal import *
getcontext().prec = 400


events = [
	'END_PROC',
	'HONEST_BLOCK',
	'ADV_BLOCK',
	]

'''
Structure of a block:
	height:<position in chain>, 
	miner:<either honest or # adversary>

Structure of a late block: 	
	delay: <Size of queue the observes on arrival - K>	

'''
def computeBlockInterval(beta):
	nextBlkTime = np.random.exponential(beta)
	return nextBlkTime

def removeEvent(event, count):
	global removedEvents
	if count not in removedEvents:
		removedEvents[count] = event
	
def deleteEventHistory(count):
	del removedEvents[count]

def computeProb(n,m):
	term1 = Decimal(1.0)
	term2 = Decimal(1.0)

	for j in range(n,n+m):
		term1 = term1*Decimal(j)/(m-(j-n))*Decimal(advFrac)
		term2 = term2*Decimal(j)/(m-(j-n))*Decimal(1-advFrac)

	for j in range(0,n):
		term1 = term1*Decimal(1-advFrac)
		term2 = term2*Decimal(advFrac)

	return term1-term2*Decimal(advFrac/(1-advFrac))

def comuteConfirmationProbsRosen(low, high, interval):
	confirmProbs = {}
	for numConfirm in range(low, high, interval):
		altProb = Decimal(math.pow(1-advFrac,numConfirm)-math.pow(advFrac,numConfirm+1)/(1-advFrac))
		for j in range(1,numConfirm+1):
			altProb = altProb + computeProb(numConfirm,j) 
		confirmProbs[numConfirm] = float(1-altProb)
	return confirmProbs

def resetAttack(time):
	global attackHead, lastAdvBlock, evCount, abCount, pQueue, removedEvents, numAttack, hiddenQueue, hiddenQueueLen
	removeEvent('ADV_BLOCK', abCount)
	hiddenQueue = []
	hiddenQueueLen = 0
	attackHead = lastHonestBlock
	lastAdvBlock = lastHonestBlock
	numAttack = numAttack + 1
	evCount = evCount + 1
	abCount = evCount
	nextAdvBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
	heapq.heappush(pQueue, [time+nextAdvBlkTime, evCount, 'ADV_BLOCK', {'height':lastHonestBlock+1, 'miner':'adv'}])

def releaseHiddenQueue(time):
	global pQueue, removedEvents, release, hstQueue, hiddenQueue, hstQueueLen, hiddenQueueLen, lateBlocks, numLateBlocks, evCount, abCount, hbCount, epCount, lastHonestBlock, attackHead, lastAdvBlock, numAttack
	
	advHead = hiddenQueue[0]['height']
	advTail = hiddenQueue[-1]['height']

	startPos = 0
	if advTail < lastHonestBlock:
		print(advTail, lastHonestBlock, "Wrong call")
		return

	if advHead > lastProcessedBlock:
		# print("advHead", advHead, "advTail", advTail, hiddenQueueLen, "lp", lastProcessedBlock)
		index = 0
		# Finding the common parent
		for index in range(0,hstQueueLen):
			if hstQueue[index]['height'] < advHead:
				continue
			break
		startPos = index
		
		# Substitute appropriate honest blocks with adversarial blocks
		# print(hiddenQueueLen, hstQueueLen)
		while index < hstQueueLen:
			hstQueue[index] = hiddenQueue[0]
			index = index + 1	
			del hiddenQueue[0]
			hiddenQueueLen = hiddenQueueLen -1

		# Adding extra honest blocks to the queue
		for i in range(0, hiddenQueueLen):
			blk = hiddenQueue[0]
			if hstQueueLen > k:
				lateBlocks.append(blk)
				numLateBlocks = numLateBlocks + 1 
			hstQueue.append(blk)
			hstQueueLen = hstQueueLen + 1
			del hiddenQueue[0]
	
		hiddenQueue = []
		hiddenQueueLen = 0
		if startPos == 0 and hstQueueLen > 0:
			removeEvent('END_PROC', epCount)
			evCount = evCount + 1 
			epCount = evCount
			heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

	else:
		# To remove the next already available end process event
		# Fill the entire hstQueue with hiddenQueue
		removeEvent('END_PROC', epCount)
		hstQueue = hiddenQueue[:]
		hstQueueLen = hiddenQueueLen
		hiddenQueue = []
		hiddenQueueLen = 0
		evCount = evCount + 1
		epCount = evCount
		heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

		if hstQueueLen > k:
			numLateBlocks = numLateBlocks + hstQueueLen - (k+1)
			for j in range(k+1, hstQueueLen):
				lateBlocks.append(hstQueue[j])
	
	removeEvent('HONEST_BLOCK', hbCount)
	lastHonestBlock = hstQueue[-1]['height']
	if hstQueueLen <= k+1:
		evCount = evCount + 1
		hbCount = evCount
		nextBlkTime = computeBlockInterval(1/honestLambd)
		heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])
	
	removeEvent('ADV_BLOCK', abCount)
	attackHead = lastHonestBlock
	lastAdvBlock = lastHonestBlock
	numAttack = numAttack + 1
	evCount = evCount + 1
	abCount = evCount
	nextAdvBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
	heapq.heappush(pQueue, [time+nextAdvBlkTime, evCount, 'ADV_BLOCK', {'height':lastHonestBlock+1, 'miner':'adv'}])

def runDST():
	
	global pQueue, numEvents, lastProcessedBlock, lastHonestBlock,lastAdvBlock, evCount, epCount, abCount, hbCount, hstQueue, hstQueueLen, attackHead, numAttack, numSuccessAttack, numUnsuccessAttack, hiddenQueue, hiddenQueueLen, numLateBlocks, lateBlocks

	while pQueue and numAttack < maxNumAttack:
		numEvents = numEvents + 1
		time, count, event, blk = heapq.heappop(pQueue)

		# Skipping Removed Elements
		if count in removedEvents:
			deleteEventHistory(count)
			continue

		if event == 'END_PROC':
			lastProcessedBlock = blk['height']
			del hstQueue[0]
			hstQueueLen = hstQueueLen - 1
			if hstQueueLen > 0:
				evCount = evCount + 1
				epCount = evCount
				heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

			if hstQueueLen == k+1:
				nextBlkTime = computeBlockInterval(1/honestLambd)
				evCount = evCount + 1
				hbCount = evCount
				heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])	


		elif event == 'HONEST_BLOCK':
			hstQueue.append(blk)
			hstQueueLen = hstQueueLen + 1

			if blk['height'] > lastHonestBlock:
				lastHonestBlock = blk['height']
			else:
				print("Panic..!!!! A honest block with lower height has been generated")
			
			if hstQueueLen > k+1:
				lateBlocks.append(blk)
				numLateBlocks = numLateBlocks + 1
			else:
				nextBlkTime = computeBlockInterval(1/honestLambd)
				evCount = evCount + 1
				hbCount = evCount
				heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])

			if hstQueueLen == 1:
				evCount = evCount + 1
				epCount = evCount
				heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', blk])

			if lastHonestBlock - attackHead >= constTh:
				if lastAdvBlock == lastHonestBlock+1:
					numSuccessAttack = numSuccessAttack + 1
					# resetAttack(time)
					# continue
					releaseHiddenQueue(time)
					continue

				honestAdvantage = lastHonestBlock - lastAdvBlock
				if honestAdvantage > resetTh:
					numUnsuccessAttack = numUnsuccessAttack + 1
					resetAttack(time)
		
		elif event == 'ADV_BLOCK':
			lastAdvBlock = blk['height']
			hiddenQueue.append(blk)
			hiddenQueueLen = hiddenQueueLen + 1
			if lastHonestBlock - attackHead >= constTh:
				if lastAdvBlock == lastHonestBlock+1:
					numSuccessAttack = numSuccessAttack + 1
					releaseHiddenQueue(time)
					# resetAttack(time)
					continue	
			
			evCount = evCount + 1
			abCount = evCount
			nextBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
			heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'ADV_BLOCK', {'height':lastAdvBlock+1, 'miner':'adv'}])
		else:
			print("Unknown event: ", event, " found. Exiting...")
			exit()

def runDS():
	global pQueue, numEvents, lastProcessedBlock, lastHonestBlock,lastAdvBlock, evCount, epCount, abCount, hbCount, hstQueue, hstQueueLen, attackHead, numAttack, numSuccessAttack, numUnsuccessAttack

	while pQueue and numAttack < maxNumAttack:
		numEvents = numEvents + 1
		time, count, event, blk = heapq.heappop(pQueue)

		# Check whether the event is already removed or not
		# If the event is removed discard its affects.
		if count in removedEvents:
			deleteEventHistory(count)
			continue

		if event == 'END_PROC':
			lastProcessedBlock = blk['height']
			del hstQueue[0]
			hstQueueLen = hstQueueLen - 1
			if hstQueueLen > 0:
				evCount = evCount + 1
				epCount = evCount
				heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

			if hstQueueLen == k+1:
				nextBlkTime = computeBlockInterval(1/honestLambd)
				evCount = evCount + 1
				hbCount = evCount
				heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])	


		elif event == 'HONEST_BLOCK':
			hstQueue.append(blk)
			hstQueueLen = hstQueueLen + 1

			if blk['height'] > lastHonestBlock:
				lastHonestBlock = blk['height']
			else:
				print("Panic..!!!! A honest block with lower height has been generated")
			
			nextBlkTime = computeBlockInterval(1/honestLambd)
			evCount = evCount + 1
			hbCount = evCount
			heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])

			if hstQueueLen == 1:
				evCount = evCount + 1
				epCount = evCount
				heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', blk])

			if lastHonestBlock - attackHead >= constTh:
				if lastAdvBlock > lastHonestBlock:
					numSuccessAttack = numSuccessAttack + 1
					resetAttack(time)

				honestAdvantage = lastHonestBlock - lastAdvBlock
				if honestAdvantage > resetTh:
					numUnsuccessAttack = numUnsuccessAttack + 1
					resetAttack(time)
		
		elif event == 'ADV_BLOCK':
			lastAdvBlock = blk['height']
			if lastHonestBlock - attackHead >= constTh:
				if lastAdvBlock > lastHonestBlock:
					numSuccessAttack = numSuccessAttack + 1
					resetAttack(time)
					continue	
			evCount = evCount + 1
			abCount = evCount
			nextBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
			heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'ADV_BLOCK', {'height':lastAdvBlock+1, 'miner':'adv'}])
		else:
			print("Unknown event: ", event, " found. Exiting...")
			break

def initQueue():
	global evCount, abCount, hbCount
	honestTime = computeBlockInterval(1/honestLambd)
	advTime = computeBlockInterval(1/(advFrac*globalLambd))
	hbCount = evCount
	heapq.heappush(pQueue, [honestTime, evCount, 'HONEST_BLOCK', {'height':1, 'miner':'honest'}])
	evCount = evCount + 1
	abCount = evCount
	heapq.heappush(pQueue, [advTime, evCount, 'ADV_BLOCK', {'height':1, 'miner':'adv'}])

def printExptInfo():
	print("-----------------------------------")
	print("Adversarial Strategy: "+strategy)
	print("Global Inter arrival: "+str(1/globalLambd))
	print("Adversary fraction: "+str(advFrac))
	print("Block Processing Time: "+str(tau))
	# print("K:"+str(k)+"\t maximum K+N: "+str('unbounded'))
	print("-----------------------------------")
	print("itr,QueueLen,ConstTh,ResetTh,NumBlocks,NumAttack,NumSuccessAttack,fracSuccessAttack,SimTime")

def writeExptInfo(file):
	file.write("-----------------------------------\n")
	file.write("Adversarial Strategy: "+strategy+"\n")
	file.write("Global Inter arrival: "+str(1/globalLambd)+"\n")
	file.write("adversary fraction: "+str(advFrac)+"\n")
	file.write("Block Processing Time: "+str(tau)+"\n")
	file.write("-----------------------------------\n")
	file.write("itr,QueueLen,ConstTh,ResetTh,NumBlocks,NumAttack,NumSuccessAttack,fracSuccessAttack,SimTime\n")
	file.close()

def printResult(itr):
	# print(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(simTime))
	print(str(itr)+","+str(k)+","+str(constTh)+","+str(resetTh)+","+str(lastHonestBlock)+","+str(numAttack)+","+str(numSuccessAttack)+","+str(numSuccessAttack/numAttack)+","+str(simTime))

def writeResult(file, itr):
	file.write(str(itr)+","+str(k)+","+str(constTh)+","+str(resetTh)+","+str(lastHonestBlock)+","+str(numAttack)+","+str(numSuccessAttack)+","+str(numSuccessAttack/numAttack)+","+str(simTime)+"\n")
	file.close()

advFrac = 0.30
tau = 5.0
honestLambd = 1.0/15.0
globalLambd = honestLambd/(1-advFrac)

if len(sys.argv) < 3:
	print ('dst')
	exit()
dst = (sys.argv[2] == 'dst')
print(dst)


maxNumAttack = int(sys.argv[1])
release = False
outFilePath =''
strategy = 'ds'

confirmProbsRosen = comuteConfirmationProbsRosen(5,30,5)
print(confirmProbsRosen)
# exit()
printExptInfo()

for k in range(15,70,10):
	for j in range(15,70,10):
		outFilePath = os.environ["HOME"]+"//EVD-Expt/des/dsData/k"+str(k)+"/sim-res-"+str(strategy)+str(j)+".txt"
		outFile = open(outFilePath, "a+")
		writeExptInfo(outFile)
		numRuns = 100
		constTh = j
		resetThs = [j/2,j,2*j,4*j,8*j]
		# resetThs = [j,2*j]
		for resetTh in resetThs:
			# avgSuccessProb = 0.0
			for i in range(0, numRuns, 1):
				np.random.seed(i+1000)
				pQueue = []
				hstQueue = []
				hiddenQueue = []
				hstQueueLen = hiddenQueueLen = 0
				lastProcessedBlock = lastHonestBlock = 0
				numSuccessAttack = numUnsuccessAttack = attackHead = lastAdvBlock = 0
				numAttack = 0
				lateBlocks = []
				numLateBlocks = 0
				
				numEvents = 0
				evCount = 0
				epCount = abCount = hbCount = -1
				removedEvents = {}
				startTime = time.clock()
				initQueue()
				if dst:
					runDST()
				else:
					runDS()
				simTime = time.clock()-startTime
				# avgSuccessProb = avgSuccessProb + (numSuccessAttack/numAttack)
				outFile = open(outFilePath, "a+")
				writeResult(outFile, i)
				printResult(i)
				# print(i,numSuccessAttack,numAttack)
			# print(constTh,resetTh,k,avgSuccessProb/numRuns,numLateBlocks/lastHonestBlock)