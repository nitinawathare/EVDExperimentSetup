SERVER_LIST=ipList

while read REMOTE_SERVER
do
	echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 2 /home/ubuntu/gitRepoEVD/queuLengthStats" )"\n\n" &
		
done < $SERVER_LIST

