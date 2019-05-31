#!/bin/bash

SERVER_LIST=ipList

#sh staticJsonRead.sh > static.txt
#sh staticJsonRead1.sh > static1.txt
echo "copied static.json"
#sh addressRead.sh > address.txt
echo "copied addreses"

#python buildGenesis.py > genesis.json
echo "build genesis"

#python formStaticJson.py 
#python formStaticJson1.py
echo "formed static.json" 

var=0
hashPowerVar=0
#rm -r Logs
#mkdir Logs

while read REMOTE_SERVER
do
	#echo staticJsonFiles/static.json$var 	
	#scp -i quorum2.key staticJsonFiles/static.json$var ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/.ethereum/static-nodes.json &
	

	#scp -i quorum2.key staticJsonFiles/static.json$var"_"$var ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/.ethereum1/static-nodes.json &
	
	#scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	#scp -i quorum2.key /home/nitin14/NewEVD/EVD-Prototype/scripts/automate2.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/scripts/automate2.py
	#echo "processing *********"$REMOTE_SERVER
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f automate2.py;"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/chaindata/"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/lightchaindata/"
	hashPowerVar=$(sed  "$((var+1))q;d" /home/nitin14/NewEVD/EVDExperimentSetup/hashPower)
	echo "hashPower $hashPowerVar"
	#echo "new hashpower calculated is "
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "nohup killall geth; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/chaindata/; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/lightchaindata/; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --k 10 init /home/ubuntu/gitRepoEVD/genesis.json; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --rpc --rpcport 22000 --port 21000 --verbosity 3 --gcmode archive --hashpower $hashPowerVar --k 10 --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt" > /home/nitin14/NewEVD/EVDExperimentSetup/Logs/log$var.txt 2>&1 &


	ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum1/geth/chaindata/; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum1/geth/lightchaindata/; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum1 --k 10 init /home/ubuntu/gitRepoEVD/genesis.json; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum1 --rpc --rpcport 22001 --port 21001 --verbosity 3 --gcmode archive --hashpower $hashPowerVar --k 10 --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt" > /home/nitin14/NewEVD/EVDExperimentSetup/Logs/log$var"_"$var.txt 2>&1 &


	#echo "after starting ************ "$REMOTE_SERVER
	#sleep 2s
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --rpc --rpcport 22001 --port 21000 --verbosity 4 --gcmode archive --hashpower 7.1 --k 10 --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt" > log$var.txt 2>&1 &
	# echo "after start************ "$REMOTE_SERVER
	var=$((var+1))
	#echo $var
done < $SERVER_LIST
