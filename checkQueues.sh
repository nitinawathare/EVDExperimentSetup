SERVER_LIST=ipList

while read REMOTE_SERVER
do
	# echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/executionTime" )"\n\n" &

	echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/queuLengthStats" ) &
	# echo $REMOTE_SERVER ":" $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "tail -n 1 /home/ubuntu/gitRepoEVD/minersInChain" ) &
		
done < $SERVER_LIST

