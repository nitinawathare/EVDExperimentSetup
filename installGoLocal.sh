#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
        ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sh /home/ubuntu/gitRepoEVD/installGo.sh"
done < $SERVER_LIST

