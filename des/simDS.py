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
	# if beta < 20 and nextBlkTime > 100:
	# 	print(beta, nextBlkTime)
	return nextBlkTime

def removeEvent(event, count):
	if count not in removedEvents:
		removedEvents[count] = event
	
def deleteEventHistory(count):
	# if count in removedEvents:
	del removedEvents[count]

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
		# if numEvents %10000 == 0:
		# 	print(numEvents)

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
			
			if hstQueueLen <= k+1:
				nextBlkTime = computeBlockInterval(1/honestLambd)
				evCount = evCount + 1
				hbCount = evCount
				heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])

			if hstQueueLen == 1:
				evCount = evCount + 1
				epCount = evCount
				heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', blk])

			if lastHonestBlock - attackHead > constTh:
				if lastAdvBlock > lastHonestBlock:
					# print(lastAdvBlock, lastHonestBlock, attackHead)
					numSuccessAttack = numSuccessAttack + 1
					resetAttack(time)

				honestAdvantage = lastHonestBlock - lastAdvBlock
				if hstQueueLen <= k+1 and honestAdvantage > resetTh:
					numUnsuccessAttack = numUnsuccessAttack + 1
					resetAttack(time)
		
		elif event == 'ADV_BLOCK':
			lastAdvBlock = blk['height']
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
	print("K:"+str(k)+"\t maximum K+N: "+str('unbounded'))
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
	print(str(numSuccessAttack/numAttack))

def writeResult(file, itr):
	# file.write(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(simTime)+"\n")
	file.close()

advFrac = 1.0/3.0
tau = 5.0
honestLambd = 1.0/15.0
globalLambd = honestLambd/(1-advFrac)

if len(sys.argv) < 3:
	print ('maxNumAttack')

maxNumAttack = int(sys.argv[1])
release = False
outFilePath =''
strategy = 'consistency'

for k in range(5,50,10):
	outFilePath = os.environ["HOME"]+"/EVD-Expt/data/simDS/sim-res-"+str(strategy)+str(k)+".txt"
	outFile = open(outFilePath, "a+")
	# print(outFilePath)
	printExptInfo()
	writeExptInfo(outFile)
	for i in range(0, 10, 1):
		np.random.seed(i)
		pQueue = []
		hstQueue = []
		hstQueueLen = 0
		lastProcessedBlock = lastHonestBlock = 0
		numSuccessAttack = numUnsuccessAttack = attackHead = lastAdvBlock = 0
		numAttack = 0
		constTh = k/2
		resetTh = k/2
		numEvents = 0
		evCount = 0
		epCount = abCount = hbCount = -1
		removedEvents = {}

		startTime = time.clock()
		initQueue()
		run()
		simTime = time.clock()-startTime
		printResult(i)
		outFile = open(outFilePath, "a+")
		writeResult(outFile, i)