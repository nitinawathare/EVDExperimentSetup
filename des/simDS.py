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
	global attackHead, lastAdvBlock, evCount, abCount, pQueue, numAttack
	removeEvent('ADV_BLOCK', abCount)
	attackHead = lastHonestBlock
	lastAdvBlock = lastHonestBlock
	numAttack = numAttack + 1
	evCount = evCount + 1
	abCount = evCount
	nextAdvBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
	heapq.heappush(pQueue, [time+nextAdvBlkTime, evCount, 'ADV_BLOCK', {'height':lastHonestBlock+1, 'miner':'adv'}])

def run():
	
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

			# if hstQueueLen == k+1:
			# 	nextBlkTime = computeBlockInterval(1/honestLambd)
			# 	evCount = evCount + 1
			# 	hbCount = evCount
			# 	heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])	


		elif event == 'HONEST_BLOCK':
			hstQueue.append(blk)
			hstQueueLen = hstQueueLen + 1

			if blk['height'] > lastHonestBlock:
				lastHonestBlock = blk['height']
			else:
				print("Panic..!!!! A honest block with lower height has been generated")
			
			# if hstQueueLen <= k+1:
			nextBlkTime = computeBlockInterval(1/honestLambd)
			evCount = evCount + 1
			hbCount = evCount
			heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])
			# else:
				# print("Honest Queue size",hstQueueLen)

			if hstQueueLen == 1:
				evCount = evCount + 1
				epCount = evCount
				heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', blk])

			if lastHonestBlock - attackHead >= constTh:
				if lastAdvBlock > lastHonestBlock:
					# print(lastAdvBlock, lastHonestBlock, attackHead)
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
	print("QueueLen,ConstTh,ResetTh,NumBlocks,NumAttack,NumSuccessAttack,fracSuccessAttack,SimTime")

def writeExptInfo(file):
	# file.write("-----------------------------------\n")
	# file.write("Adversarial Strategy: "+strategy+"\n")
	# file.write("Global Inter arrival: "+str(1/globalLambd)+"\n")
	# file.write("K:"+str(k)+"\t maximum K+N: "+str('unbounded')+"\n")
	# file.write("adversary fraction: "+str(advFrac)+"\n")
	# file.write("Block Processing Time: "+str(tau)+"\n")
	# file.write("-----------------------------------\n")
	# file.write("QueueLen,ConstTh,ResetTh,NumBlocks,NumAttack,NumSuccessAttack,fracSuccessAttack,SimTime\n")
	file.close()

def printResult(itr):
	# print(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(simTime))
	print(str(itr)+","+str(k)+","+str(constTh)+","+str(resetTh)+","+str(lastHonestBlock)+","+str(numAttack)+","+str(numSuccessAttack)+","+str(numAttack/numSuccessAttack)+","+str(simTime))

def writeResult(file, itr):
	# file.write(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(simTime)+"\n")
	file.close()

advFrac = 0.30
tau = 0.001
honestLambd = 1.0/15.0
globalLambd = honestLambd/(1-advFrac)

if len(sys.argv) < 3:
	print ('maxNumAttack')

maxNumAttack = int(sys.argv[1])
release = False
outFilePath =''
strategy = 'consistency'

confirmProbsRosen = comuteConfirmationProbsRosen(5,30,5)
print(confirmProbsRosen)
# exit()
printExptInfo()
for j in range(5,30,5):
	# outFilePath = os.environ["HOME"]+"/EVD-Expt/data/simDS/sim-res-"+str(strategy)+str(k)+".txt"
	# outFile = open(outFilePath, "a+")
	# writeExptInfo(outFile)
	numRuns = 10
	constTh = j
	# resetThs = [j/4,j/2,j,2*j,4*j,5*j,6*j,7*j,8*j,9*j,10*j]
	resetThs = [j/4, j, 2*j, 4*j, 10*j]
	k=100
	for resetTh in resetThs:
		avgSuccessProb = 0.0
		for i in range(0, numRuns, 1):
			np.random.seed(i+1000)
			pQueue = []
			hstQueue = []
			hstQueueLen = 0
			lastProcessedBlock = lastHonestBlock = 0
			numSuccessAttack = numUnsuccessAttack = attackHead = lastAdvBlock = 0
			numAttack = 0
			
			numEvents = 0
			evCount = 0
			epCount = abCount = hbCount = -1
			removedEvents = {}
			startTime = time.clock()
			initQueue()
			run()
			simTime = time.clock()-startTime
			avgSuccessProb = avgSuccessProb + (numSuccessAttack/numAttack)
			# outFile = open(outFilePath, "a+")
			# writeResult(outFile, i)
			# printResult(i)
			# print(i,numSuccessAttack,numAttack)
		print(constTh,resetTh,k,avgSuccessProb/numRuns)