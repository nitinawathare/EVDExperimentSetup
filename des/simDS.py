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

def releaseHiddenQueueReset(time):
	global release, hstQueue, hiddenQueue, hstQueueLen, numLateBlocks, hiddenQueueLen, evCount, abCount, hbCount, epCount, lastHonestBlock
	
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
	if hstQueueLen > k:
		if mine:
			release = True
	
	if hstQueueLen <= k+1:
		evCount = evCount + 1
		hbCount = evCount
		nextBlkTime = computeBlockInterval(1/honestLambd)
		heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])
	
	removeEvent('ADV_BLOCK', abCount)
	evCount = evCount + 1
	abCount = evCount
	nextAdvBlkTime = computeBlockInterval(1/(advFrac*honestLambd))
	heapq.heappush(pQueue, [time+nextAdvBlkTime, evCount, 'ADV_BLOCK', {'height':lastHonestBlock+1, 'miner':'adv'}])

def run():
	
	global pQueue, numEvents, lastProcessedBlock, lastHonestBlock, evCount, epCount, abCount, hbCount, hstQueue, hiddenQueue, lateBlocks, numLateBlocks,hstQueueLen, hiddenQueueLen, release

	while pQueue and lastHonestBlock < maxNumBlocks:
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

			if (hiddenQueueLen == 0):
				hiddenQueue = []
				hiddenQueueLen = 0
				removeEvent('ADV_BLOCK', abCount)
				nextAdvBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
				evCount = evCount + 1
				abCount = evCount
				heapq.heappush(pQueue, [time+nextAdvBlkTime, evCount, 'ADV_BLOCK', {'height':lastHonestBlock+1, 'miner':'adv'}])

			elif (hiddenQueueLen == 1):
				releaseHiddenQueueReset(time)

			elif (hiddenQueueLen > 1) and (hiddenQueue[-1]['height'] == lastHonestBlock + 1):
				releaseHiddenQueueReset(time)
		
		elif event == 'ADV_BLOCK':
			nextBlkHeight = 0
			if lastHonestBlock >= blk['height']:
				hiddenQueue = []
				hiddenQueueLen = 0
				nextBlkHeight = lastHonestBlock + 1
			else:
				if release:
					if hstQueueLen > k:
						hstQueue.append(blk)
						hstQueueLen = hstQueueLen + 1
						lastHonestBlock = blk['height']
						nextBlkHeight = lastHonestBlock + 1
						numLateBlocks = numLateBlocks + 1
						lateBlocks.append(blk)
						removeEvent('HONEST_BLOCK', hbCount)
					else:
						release = False
				if not release:
					hiddenQueue.append(blk)
					hiddenQueueLen = hiddenQueueLen + 1
					nextBlkHeight = blk['height'] + 1
					# if hiddenQueueLen == M:
					# 	print("released chain of length ", M)
					# 	releaseHiddenQueueReset(time)	
					# 	continue
			evCount = evCount + 1
			abCount = evCount
			nextBlkTime = computeBlockInterval(1/(advFrac*globalLambd))
			heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'ADV_BLOCK', {'height':nextBlkHeight, 'miner':'adv'}])
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
	print("Iteration,NumBlocks,NumLateBlocks,fracLateBlocks,SimTime")

def writeExptInfo(file):
	file.write("-----------------------------------\n")
	file.write("Adversarial Strategy: "+strategy+"\n")
	file.write("Global Inter arrival: "+str(1/globalLambd)+"\n")
	file.write("K:"+str(k)+"\t maximum K+N: "+str('unbounded')+"\n")
	file.write("adversary fraction: "+str(advFrac)+"\n")
	file.write("Block Processing Time: "+str(tau)+"\n")
	file.write("-----------------------------------\n")
	file.write("Iteration,NumBlocks,NumLateBlocks,fracLateBlocks,SimTime\n")
	file.close()

def printResult(itr):
	print(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(simTime))

def writeResult(file, itr):
	file.write(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(simTime)+"\n")
	file.close()


advFrac = 1.0/3.0
tau = 5.0
honestLambd = 1.0/15.0
globalLambd = honestLambd/(1-advFrac)

if len(sys.argv) < 3:
	print ('maxNumBlocks \n mine')

maxNumBlocks = int(sys.argv[1])
release = False
strategy = ''
outFilePath =''s
strategy = 'consistency'

for k in range(25,85,10):
	outFilePath = os.environ["HOME"]+"/EVD-Expt/data/simDS/sim-res-"+str(strategy)+str(k)+".txt"
	outFile = open(outFilePath, "a+")
	print(outFilePath)
	printExptInfo()
	writeExptInfo(outFile)
	for i in range(0, 100, 1):
		np.random.seed(i)
		pQueue = []
		hstQueue = []
		hstQueueLen = 0
		lastProcessedBlock = lastHonestBlock = 0
		attackHead = lastAdvBlock = 0

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