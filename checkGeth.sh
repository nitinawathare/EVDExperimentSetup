
#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep geth | wc -l" ) " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep automate2 | wc -l" ) &
	
done < $SERVER_LIST

