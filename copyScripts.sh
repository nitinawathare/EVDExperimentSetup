
#!/bin/bash
SERVER_LIST=ipList

folder=$(date +%d-%m-%Y-%H-%M-%S)		
var=0


# mkdir /home/sourav/EVD-Data/$folder
# mkdir /home/sourav/EVD-Data/$folder/Mi
# mkdir /home/sourav/EVD-Data/$folder/Mc
# mkdir /home/sourav/EVD-Data/$folder/Log
# mkdir /home/sourav/EVD-Data/$folder/Ex
# mkdir /home/sourav/EVD-Data/$folder/Ti

while read REMOTE_SERVER
do
	 #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r gitRepoEVD" 
	 #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "mkdir gitRepoEVD" 
 	#scp -i quorum2.key addressRead.py staticJsonRead.py staticJsonRead1.py passwords.txt installGo.sh downloadEVDCode.sh downloadEVDCode2.sh setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&

 	# scp -i quorum2.key deployContract.py sendTransaction.py cpuheavy.sol matrixMultiplication.sol emptyLoop.sol ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&	
 	
 	# scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&


    # scp -r -i quorum2.key /home/sourav/EVD-Prototype/scripts ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/&

	# mkdir ~/VMQuorumNode/Node$REMOTE_SERVER
	# scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/miningInfo /home/sourav/EVD-Data/$folder/Mi/$var.dat & 
	# scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/minersInChain /home/sourav/EVD-Data/$folder/Mc/$var.dat & 
	# scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/log.txt /home/sourav/EVD-Data/$folder/Log/$var.txt & 
	# scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/executionTime /home/sourav/EVD-Data/$folder/Ex/$var.txt & 
	# scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/experimentTimeStats /home/sourav/EVD-Data/$folder/Ti/$var.txt & 

	#scp -i quorum2.key /home/nitin14/NewEVD/EVD-Prototype/scripts/automate2.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/scripts/automate2.py &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/queuLengthStats" &
	# ssh -o StrictHostKeyChecking=no -l sourav $REMOTE_SERVER&
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/miningInfo" &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/minersInChain" &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/log.txt" &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/executionTime" &
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/experimentTimeStats" &

	

	#scp -i quorum2.key installpy3.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	#scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
        #scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key downloadEVDCode.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	 
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json"

	var=$((var+1))
done < $SERVER_LIST

