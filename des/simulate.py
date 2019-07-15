'''

This file is the discrete event simulator 
for adversarial strategy reset.

'''
import sys
import time
import math 
import numpy as np
import os

from decimal import *
getcontext().prec = 400


events = [
	'START_PROC',
	'END_PROC',
	'HONEST_BLOCK',
	'ADV_BLOCK',
	'RELEASE'
	]

'''
Structure of a block:
	height:<position in chain>, 
	miner:<either honest or # adversary>

Structure of a late block: 	
	delay: <Size of queue the observes on arrival - K>	

'''

def releaseHiddenQueueReset(time):
	advHead = hiddenQueue[0]['height']
	initHstLen = len(hstQueue)
	if advHead > lastProcessedBlock:
		index = 0
		for index in range(0,hstQueueLen):
			if hstQueue[index]['height'] < advHead:
				continue
			break
		while blk in hiddenQueueLen:
			hstQueue[index] = blk
			index = index + 1
			if index >= k:
				lateBlocks.append(blk)
				numLateBlocks = numLateBlocks + 1 
			hiddenQueue.delete(0)
		hstQueueLen = len(hstQueue)
		if initHstLen == 0 and hstQueueLen > 0:
			heappush(pQueue, [time+tau,'END_PROCESS', hstQueue[0]])
	if advHead < lastProcessedBlock:
		

		
hstQueue = []
hstQueueLen = len(hstQueue)

hiddenQueue = []
hiddenQueueLen = len(hiddenQueue)

lateBlocks = []
numLateBlocks = len(lateBlocks)

advFrac = 1.0/3.0
tau = 5.0
honestLambd = 1.0/15.0
globalLambd = honestLambd/(1-advFrac)
k = 3
lastProcessedBlock = 0

pQueue = []
epsilon = 10**(-10)

while pQueue:
	time, event, blk = heappop(pQueue)
	if event == 'START_PROC':
		heappush([time+tau, 'END_PROC'])
	
	elif event == 'END_PROC':
		hstQueue.delete(0)
		hstQueueLen = hstQueueLen - 1
		if len(hstQueue > 0):
			heappush([time+tau, 'END_PROC', blk])

	elif event == 'HONEST_BLOCK':
		
		if hstQueueLen > k:
			lateBlocks.append([blk, hstQueueLen])

		hstQueue.append(blk)
		hstQueueLen = hstQueueLen + 1
		if hstQueueLen == 1:
			heappush([time+tau, 'END_PROC', blk])

		if lenHiddenQueue == 1:
			releaseHiddenQueueReset()

		if hiddenQueue[-1]['height'] = blk['height'] + 1:
			releaseHiddenQueueReset()

		nextBlkTime = exp(honestLambd)
		heappush([time+nextBlkTime, {'height':blk[0]+1, 'miner':'honest'}])

	elif event == 'ADV_BLOCK':

		
	elif event == 'RELEASE':
		####
	else:
		print("Unknown event: ", event, " found. Exiting...")
		break