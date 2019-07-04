#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	if [ "$1" = "install" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup sudo apt install ntp -y; nohup sudo service ntp start; nohup timedatectl set-ntp true" &

	elif [ "$1" = "sync" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo service ntp stop; sudo ntpd -gq; sudo service ntp start" &

	elif [ "$1" = "check" ]; then
		echo $REMOTE_SERVER " : " $(ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "timedatectl | grep 'NTP synchronized:'") &

	else 
		echo "
		'install'		to install tools required for ntp sync
		'sync'			to sync ndoes
		'check'			to check status
		"
		break
	fi	
done < $SERVER_LIST