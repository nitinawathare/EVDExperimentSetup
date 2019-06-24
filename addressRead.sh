#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER

do
    #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sh /home/ubuntu/gitRepoEVD/startScript.sh"&
	#echo "inside **********2"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "python /home/ubuntu/gitRepoEVD/addressRead.py"
	#echo "inside **********1"
done < $SERVER_LIST


