
#!/bin/bash

SERVER_LIST=ipList

while read REMOTE_SERVER
do
        ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sudo tc qdisc del dev eth0 root" &
done < $SERVER_LIST
