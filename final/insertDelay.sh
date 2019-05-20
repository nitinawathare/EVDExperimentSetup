SERVER_LIST=ipList

while read REMOTE_SERVER
do
	echo serving $REMOTE_SERVER	
	
done < $SERVER_LIST
