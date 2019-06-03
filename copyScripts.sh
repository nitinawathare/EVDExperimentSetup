
#!/bin/bash
SERVER_LIST=ipList

folder=$(date +%H-%M-%S-%d-%m-%Y)
var=0

# mkdir /home/sourav/EVD-Data/$folder

while read REMOTE_SERVER
do
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r gitRepoEVD" 
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "mkdir gitRepoEVD" 
 	#scp -i quorum2.key addressRead.py staticJsonRead.py staticJsonRead1.py passwords.txt installGo.sh downloadEVDCode.sh downloadEVDCode2.sh setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&
    # scp -r -i quorum2.key /home/sourav/EVD-Prototype/scripts ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/&
	# scp -i quorum2.key /home/sourav/EVD-Prototype/scripts/automate2.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/scripts/automate2.py &
	scp -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/queuLengthStats /home/sourav/EVD-Data/$folder/queuLengthStats$var.dat &
	
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/queuLengthStats" &
	#scp -i quorum2.key passwords.txt ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
        #scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key downloadEVDCode.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	 
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json"

	var=$((var+1))
done < $SERVER_LIST

