#!/bin/bash

SERVER_LIST=ipList

sh staticJsonRead.sh > static.txt
sh addressRead.sh > address.txt

#echo "************** here2"
python buildGenesis.py > genesis.json

#echo "************** here1"
while read REMOTE_SERVER
do
        scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
        ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json"
done < $SERVER_LIST
