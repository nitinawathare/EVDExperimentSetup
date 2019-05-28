#!/bin/bash

SERVER_LIST=ipList

#sh staticJsonRead.sh > static.txt
#sh addressRead.sh > address.txt


echo "************** here2"
python buildGenesis.py > genesis.json

python formStaticJson.py 
echo "************** here1"
var=0
while read REMOTE_SERVER
do
	#echo staticJsonFiles/static.json$var 	
	#scp -i quorum2.key staticJsonFiles/static.json$var ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/.ethereum/static-nodes.json
	#scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	echo "processing *********"$REMOTE_SERVER
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f automate2.py;"
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/chaindata/"
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --k 10 init /home/ubuntu/gitRepoEVD/genesis.json"
	echo "after init************ "$REMOTE_SERVER
	sleep 2s
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --rpc --rpcport 22001 --port 21000 --verbosity 4 --hashpower 7.1 --k 10 --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt 2>>1.log &" &
	echo "after start************ "$REMOTE_SERVER
	var=$((var+1))
done < $SERVER_LIST

#sh insertDelay.sh
