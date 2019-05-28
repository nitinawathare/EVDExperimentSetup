SERVER_LIST=ipList



while read REMOTE_SERVER
do
	echo "processing "$REMOTE_SERVER
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo tc qdisc del dev eth0 root"
	
done < $SERVER_LIST
