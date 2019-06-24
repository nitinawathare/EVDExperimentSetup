#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	if [ "$1" = "ex" ]; then
		echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/executionTime" ) &

	elif [ "$1" = "pp" ]; then
		echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/processPreviousTime" ) &

	elif [ "$1" = "mc" ]; then
		echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/minersInChain" ) &

	elif [ "$1" = "mi" ]; then
		echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/miningInfo" ) &

	elif [ "$1" = "qs" ]; then 
		echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/queuLengthStats" ) &

	else 
		echo "
		'ex'		for executionTime
		'pp'		for processPreviousTime
		'mc'		for minersInChain
		'mi'		for miningInfo
		'qs'		for queuLengthStats
		"
		break
	fi	
done < $SERVER_LIST

