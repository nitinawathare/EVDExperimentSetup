#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	echo $REMOTE_SERVER " : "$(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "python3 /home/ubuntu/gitRepoEVD/EVD-Prototype/scripts/automate2.py")&
done < $SERVER_LIST
