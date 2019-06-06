SERVER_LIST=ipList

while read REMOTE_SERVER
do
	echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 100 /home/ubuntu/error1.log" )"\n\n" &
		
done < $SERVER_LIST

