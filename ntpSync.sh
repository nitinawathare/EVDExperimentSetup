#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	echo $REMOTE_SERVER
	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sudo apt install ntp -y; nohup sudo service ntp start; nohup timedatectl set-ntp true"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "ps -ax | grep automate2.py | wc" &
done < $SERVER_LIST