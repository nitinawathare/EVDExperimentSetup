
SERVER_LIST=ipList

while read REMOTE_SERVER
do

# echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --exec 'net.peerCount' attach ipc:/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc") &

echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --exec 'eth.blockNumber' attach ipc:/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc") &

#echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --exec 'eth.mining' attach ipc:/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc") &

# echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --exec 'eth.syncing' attach ipc:/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc") &

# echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --exec 'miner.start()' attach ipc:/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc") &

# echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --exec 'miner.stop()' attach ipc:/home/ubuntu/gitRepoEVD/.ethereum/geth.ipc") &

done < $SERVER_LIST
