#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	# echo $REMOTE_SERVER
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sudo apt install ntp -y; nohup sudo service ntp start; nohup timedatectl set-ntp true" &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "timedatectl" &

	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo service ntp stop; sudo ntpd -gq; sudo service ntp start" &
	echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "timedatectl | grep 'NTP synchronized: no'") &
done < $SERVER_LIST