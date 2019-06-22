#!/bin/bash

SERVER_LIST=ipList

while read REMOTE_SERVER
do
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth" &
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall git" &
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f deployEVDContract.py;" &
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f sendEVDTransaction.py;" &
done < $SERVER_LIST
