#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	if [ "$1" = "deploy" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup python3 /home/ubuntu/gitRepoEVD/deployContract.py"&

	elif [ "$1" = "send" ]; then
		nohup ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup python3 /home/ubuntu/gitRepoEVD/sendTransaction.py"&
	
	elif [ "$1" = "deployevd" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup python3 /home/ubuntu/gitRepoEVD/deployEVDContract.py"&

	elif [ "$1" = "sendevd" ]; then
		nohup ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup python3 /home/ubuntu/gitRepoEVD/sendEVDTransaction.py"&
	
	elif [ "$1" = "stop" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "python3 /home/ubuntu/gitRepoEVD/stopExperiment.py"&
	else
		echo "
			'deploy'		To run deployContract.py
			'send'			To run sendTransaction.py
			'deployevd'		To run deployEVDContract.py
			'sendevd'		To run sendEVDTransaction.py
		"
		break
	fi
done < $SERVER_LIST
