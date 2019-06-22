
#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	# echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep geth | wc -l" ) " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep deployContract | wc -l" ) " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep sendTransaction | wc -l" ) &
	

	echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep geth | wc -l" ) " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep deployEVDContract | wc -l" ) " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep sendEVDTransaction | wc -l" ) &
	
done < $SERVER_LIST

