
#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	 #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r gitRepoEVD" 
	 #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "mkdir gitRepoEVD" 
 	#scp -i quorum2.key addressRead.py staticJsonRead.py staticJsonRead1.py passwords.txt installGo.sh downloadEVDCode.sh downloadEVDCode2.sh setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&
    # scp -r -i quorum2.key /home/sourav/EVD-Prototype/scripts ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/&
	echo "copied file"
	mkdir ~/VMQuorumNode/Node$REMOTE_SERVER
	scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/ /home/nitin14/VMQuorumNode/Node$REMOTE_SERVER & 
	#scp -i quorum2.key /home/nitin14/NewEVD/EVD-Prototype/scripts/automate2.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/scripts/automate2.py &
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/queuLengthStats" &
	#scp -i quorum2.key installpy3.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	#scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
        #scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key downloadEVDCode.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	 
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json"
done < $SERVER_LIST

