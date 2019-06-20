#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER

do
        #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sh /home/ubuntu/gitRepoEVD/startScript.sh"&
	#echo "inside **********2"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "python /home/ubuntu/gitRepoEVD/addressRead.py"
	# scp -i quorum2.key contractAddressList ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&
	# scp -i quorum2.key sendTransaction.py matrixMultiplication.sol cpuheavy.sol ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	# scp -i quorum2.key sendTransaction.py matrixMemory.sol sortMemory.sol emptyLoop.sol ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	# scp -i quorum2.key deployContract.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	# scp -i quorum2.key stopExperiment.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	# scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/minersInChain" &


	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "python3 /home/ubuntu/gitRepoEVD/stopExperiment.py"&
	# nohup ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup python3 /home/ubuntu/gitRepoEVD/sendTransaction.py"&
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup python3 /home/ubuntu/gitRepoEVD/deployContract.py"&
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup rm /home/ubuntu/gitRepoEVD/log.txt"&
	#echo "inside **********1"
done < $SERVER_LIST


