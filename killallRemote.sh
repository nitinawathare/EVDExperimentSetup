#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	if [ "$1" = "all" ]; then	
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall git" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f deployContract.py;" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f sendTransaction.py;" &

	elif [ "$1" = "allevd" ]; then	
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall git" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f deployEVDContract.py;" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f sendEVDTransaction.py;" &
	
	elif [ "$1" = "deploy" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f deployContract.py;" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f deployEVDContract.py;" &
	
	elif [ "$1" = "send" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f sendTransaction.py;" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f sendEVDTransaction.py;" &

	elif [ "$1" = "git" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall git;" &

	elif [ "$1" = "geth" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth;" &
	
	else
		echo "
		'all'		to kill all go-ethereum
		'allevd'	to kill all EVD
		'deploy' 	to kill deployContract.py, deployEVDContract.py 
		'send'		to kill sendTransaction.py sendEVDTransaction.py
		'geth'		to kill geth
		'git'		to kill git
		"
		break
	fi
done < $SERVER_LIST
