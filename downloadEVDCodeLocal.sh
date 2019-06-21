#!/bin/bash

SERVER_LIST=ipList

while read REMOTE_SERVER
do
    # ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sh /home/ubuntu/gitRepoEVD/downloadEVDCodeGoEthereumSkip2.sh" &  
    ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sh /home/ubuntu/gitRepoEVD/downloadEVDCode2.sh" &  

done < $SERVER_LIST

