SERVER_LIST=ipList


python insertDelay.py 

var=0
while read REMOTE_SERVER
do
	echo "processing "$REMOTE_SERVER
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r /home/ubuntu/gitRepoEVD/delays; mkdir /home/ubuntu/gitRepoEVD/delays"
	scp -i quorum2.key delays/delay$var.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/delays/delay.sh
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sh /home/ubuntu/gitRepoEVD/delays/delay.sh"&
	echo serving $REMOTE_SERVER	
	var=$((var+1))
done < $SERVER_LIST
