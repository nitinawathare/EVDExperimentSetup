
#!/bin/bash
SERVER_LIST=ipList

while read REMOTE_SERVER
do
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r gitRepoEVD"
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "mkdir gitRepoEVD"
 	scp -i quorum2.key addressRead.py staticJsonRead.py passwords.txt installGo.sh downloadEVDCode.sh setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
        #scp -i quorum2.key staticJsonRead.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key passwords.txt ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
        #scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key downloadEVDCode.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	 
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json"
done < $SERVER_LIST

