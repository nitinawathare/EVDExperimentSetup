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
	miner:<either honest or adversary>

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
	global removedEvents, pQueue, release, hstQueue, hiddenQueue, hstQueueLen, numLateBlocks, hiddenQueueLen, evCount, abCount, hbCount, epCount, lastHonestBlock, latestHonestBlkTime, latestAdvBlkTime, eT
	
	advHead = hiddenQueue[0]['height']
	advTail = hiddenQueue[-1]['height']
	startPos = 0

	# If adversary is releasing a shorter chain, simulation implementation is incorrect
	if advTail < lastHonestBlock:
		print(advTail, lastHonestBlock, "Wrong call")
		return

	# Adversary head is still in the queue.
	if advHead > lastProcessedBlock:
		# print("advHead", advHead, "advTail", advTail, hiddenQueueLen, "lp", lastProcessedBlock)
		
		# Finding the common parent
		index = 0
		while index < hstQueueLen:
			if hstQueue[index]['height'] < advHead:
				index=index+1
				continue
			break
		startPos = index
		
		# print(hiddenQueueLen, hstQueueLen)
		# Substitute appropriate honest blocks with adversarial blocks
		while index < hstQueueLen:
			hstQueue[index] = hiddenQueue[0]
			index = index + 1	
			del hiddenQueue[0]
			hiddenQueueLen = hiddenQueueLen -1

		# Adding remaining adversarial block in the honest queue
		# If the block is late, then increment the count of late blocks
		for i in range(0, hiddenQueueLen):
			blk = hiddenQueue[0]
			if hstQueueLen > k:
				lateBlocks.append(blk)
				numLateBlocks = numLateBlocks + 1 
			hstQueue.append(blk)
			hstQueueLen = hstQueueLen + 1
			del hiddenQueue[0]
	
		# Reset the hidden queue of the miner.
		hiddenQueue = [] 
		hiddenQueueLen = 0

		# Clear the previous end process event and add a new event
		if startPos == 0 and hstQueueLen > 0:
			removeEvent('END_PROC', epCount)
			evCount = evCount + 1 
			epCount = evCount
			heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

	else:
		
		# To remove the next already available end process event
		removeEvent('END_PROC', epCount)

		# Fill the entire hstQueue with hiddenQueue
		hstQueue = hiddenQueue[:]
		hstQueueLen = hiddenQueueLen

		# Reset entire hidden queue of the adversary.
		hiddenQueue = []
		hiddenQueueLen = 0
		evCount = evCount + 1
		epCount = evCount
		heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

		# Todo: If hstQueueLen > k, we should remove block mining event 
		# of the honest node and instead add a empty block event.
		if hstQueueLen > k:
			numLateBlocks = numLateBlocks + hstQueueLen - (k+1)
			for j in range(k+1, hstQueueLen):
				lateBlocks.append(hstQueue[j])
	
	# Remove honest previous block mining event. 
	removeEvent('HONEST_BLOCK', hbCount)

	# Schedule the next honest block at the new height with old time
	lastHonestBlock = hstQueue[-1]['height']
	evCount = evCount + 1
	hbCount = evCount
	# If queue crosses threshold, schedule and empty block otherwise schedule an non-empty block.
	if hstQueueLen > k:
		if mine:
			release = True
		heapq.heappush(pQueue, [latestHonestBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'empty'}])
	else:
		heapq.heappush(pQueue, [latestHonestBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])

def run():
	
	global pQueue, numEvents, lastProcessedBlock, lastHonestBlock, evCount, epCount, abCount, hbCount, hstQueue, hiddenQueue, lateBlocks, emptyBlocks, numLateBlocks, numEmptyBlocks, hstQueueLen, hiddenQueueLen, latestHonestBlkTime, latestAdvBlkTime, release, eT

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

			# If honest queue has non-zero element schedule the next event for the
			# to mark the end of processing the next block
			if hstQueueLen > 0:
				# Remove all empty blocks from the honest queue
				for qHead in hstQueue:
					if qHead['miner'] == 'empty':
						del hstQueue[0]
						hstQueueLen = hstQueueLen -1
						eT = eT + 1
						continue
					break 
				
				if hstQueueLen > 0:
					evCount = evCount + 1
					epCount = evCount
					heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', hstQueue[0]])

			# When the queue hits k+1, remove event corresponding to the empty
			# block and schedule an event for non-empty block.
			if hstQueueLen == k+1:
				# To remove the empty block event	
				removeEvent('HONEST_BLOCK', hbCount) 

				# Insert a non-empty block event with the same time
				evCount = evCount + 1
				hbCount = evCount
				heapq.heappush(pQueue, [latestHonestBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])	

			# Todo: Also, we have to check that if the event lowers the block queue length
			# at the honest miner, we have to remove the empty block event and schedule an
			# non-empty block event instead.

		elif event == 'HONEST_BLOCK':

			if blk['height'] > lastHonestBlock:
				lastHonestBlock = blk['height']
			else:
				print("Panic..!!!! A honest block with lower height has been generated")

			hstQueue.append(blk)
			hstQueueLen = hstQueueLen + 1

			# Todo: Check if the block is empty, if so add it to the empty block list
			if blk['miner'] == 'empty':
				numEmptyBlocks = numEmptyBlocks + 1
				emptyBlocks.append(blk)
			

			evCount = evCount + 1
			hbCount = evCount
			nextBlkTime = computeBlockInterval(1/honestLambd)
			latestHonestBlkTime = time+nextBlkTime

			if hstQueueLen > k+1:
				lateBlocks.append(blk)
				numLateBlocks = numLateBlocks + 1
				# schedule the next empty block
				heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'empty'}])
			else:
				heapq.heappush(pQueue, [time+nextBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'honest'}])

			
			if hstQueueLen == 1:
				# If hstQueueLen is of size one, the head of the queue could not
				# be a empty block. Nevertheless, we will put a check here.
				for qHead in hstQueue:
					if qHead['miner'] == 'empty':
						del hstQueue[0]
						hstQueueLen = hstQueueLen -1
						eT = eT + 1
						continue
					break
				if hstQueueLen == 1:
					evCount = evCount + 1
					epCount = evCount
					heapq.heappush(pQueue, [time+tau, evCount, 'END_PROC', blk])

			# Reseting adversarial hidden queue (0,0) -> (0,0)
			if (hiddenQueueLen == 0):
				hiddenQueue = []
				hiddenQueueLen = 0

				removeEvent('ADV_BLOCK', abCount)
				nextAdvBlkTime = latestAdvBlkTime
				evCount = evCount + 1
				abCount = evCount
				heapq.heappush(pQueue, [nextAdvBlkTime, evCount, 'ADV_BLOCK', {'height':lastHonestBlock+1, 'miner':'adv'}])

			# (0,1) -> (1,1), Usually we will give advantage to the adversary in such situation.
			elif (hiddenQueueLen == 1):
				releaseHiddenQueueReset(time)

			# (x,x+2) -> (x+1, x+2), adversary releases its chain and all honest miners
			# adopts the adversarial chain.
			elif (hiddenQueueLen > 1) and (hiddenQueue[-1]['height'] == lastHonestBlock + 1):
				releaseHiddenQueueReset(time)
		
		elif event == 'ADV_BLOCK':
			nextBlkHeight = 0
			# If honest miners are already ahead of the adversary,
			# reset its hidden chain
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

						# Remove previous empty block and schedule a new empty block
						removeEvent('HONEST_BLOCK', hbCount)
						evCount = evCount + 1
						hbCount = evCount
						heapq.heappush(pQueue, [latestHonestBlkTime, evCount, 'HONEST_BLOCK', {'height':lastHonestBlock+1, 'miner':'empty'}])
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
			latestAdvBlkTime = time+nextBlkTime
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
	print("Iteration,NumBlocks,NumLateBlocks,fracLateBlocks,fracEmptyBlocks,SimTime")

def writeExptInfo(file):
	file.write("-----------------------------------\n")
	file.write("Adversarial Strategy: "+strategy+"\n")
	file.write("Global Inter arrival: "+str(1/globalLambd)+"\n")
	file.write("K:"+str(k)+"\t maximum K+N: "+str('unbounded')+"\n")
	file.write("adversary fraction: "+str(advFrac)+"\n")
	file.write("Block Processing Time: "+str(tau)+"\n")
	file.write("-----------------------------------\n")
	file.write("Iteration,NumBlocks,NumLateBlocks,fracLateBlocks,fracEmptyBlocks,SimTime\n")
	file.close()

def printResult(itr):
	print(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(numEmptyBlocks)+","+str(simTime))

def writeResult(file, itr):
	file.write(str(itr)+","+str(lastHonestBlock)+","+str(numLateBlocks)+","+str(numLateBlocks/lastHonestBlock)+","+str(numEmptyBlocks)+","+str(simTime)+"\n")
	file.close()


advFrac = 1.0/3.0
tau = 5.0
honestLambd = 1.0/15.0
globalLambd = honestLambd/(1-advFrac)

if len(sys.argv) < 3:
	print ('maxNumBlocks \n mine')

maxNumBlocks = int(sys.argv[1])
mine = sys.argv[2] == 'mine'
release = False
strategy = ''
outFilePath =''
if mine:
	strategy = 'mine'
else:
	strategy = 'reset'

for k in range(15,75,10):
	# outFilePath = os.environ["HOME"]+"/EVD-Expt/data/simDataUS/sim-res-"+str(strategy)+str(k)+".txt"
	outFilePath = "/home/ubuntu/evd-data/sim-res-"+str(strategy)+str(k)+".txt"
	
	outFile = open(outFilePath, "a+")
	numRuns = 10
	print(outFilePath)
	printExptInfo()
	writeExptInfo(outFile)
	for i in range(0, numRuns, 1):
		np.random.seed(i)
		pQueue = []
		hstQueue = []
		hiddenQueue = []
		lateBlocks = []
		emptyBlocks = []
		hstQueueLen = hiddenQueueLen = numLateBlocks = numEmptyBlocks = 0
		lastProcessedBlock = lastHonestBlock = 0
		latestHonestBlkTime = 0
		latestAdvBlkTime = 0
		eT = 0

		numEvents = 0
		evCount = 0
		epCount = abCount = hbCount = -1
		removedEvents = {}

		startTime = time.process_time()
		initQueue()
		run()
		simTime = time.process_time()-startTime
		printResult(i)
		outFile = open(outFilePath, "a+")
		writeResult(outFile, i)
