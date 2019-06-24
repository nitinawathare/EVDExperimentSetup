#!/bin/bash

SERVER_LIST=ipList

#sh staticJsonRead.sh > static.txt
#sh staticJsonRead1.sh > static1.txt
# echo "copied static.json"
#sh addressRead.sh > address.txt
# echo "copied addreses"

#python buildGenesis.py > genesis.json
# echo "build genesis"

#python formStaticJson.py 
#python formStaticJson1.py
# echo "formed static.json" 


# Gas Limit (Decimal to Hexa-decimal)
# 3.5M 	= 3567E0
# 12M 	= B71B00
# 40M 	= 2625A00
# 120M 	= 7270E00
# 240M	= E4E1C00
# 400M = 17D78400
# 800M	= 2FAF0800 

var=0
hashPowerVar=0
cacheVar=$((4096*4))
behavior=0
# cacheVar=2048
# rm -r GLogs
# mkdir GLogs

while read REMOTE_SERVER
do
	#echo staticJsonFiles/static.json$var 	
	# echo $REMOTE_SERVER
	#scp -i quorum2.key staticJsonFiles/static.json$var ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/.ethereum/static-nodes.json &
	

	#scp -i quorum2.key staticJsonFiles/static.json$var"_"$var ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/.ethereum1/static-nodes.json &
	
	#scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	#scp -i quorum2.key /home/nitin14/NewEVD/EVD-Prototype/scripts/automate2.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/EVD-Prototype/scripts/automate2.py
	#echo "processing *********"$REMOTE_SERVER
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "pkill -f automate2.py;"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/chaindata/"
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/lightchaindata/"
	hashPowerVar=$(sed  "$((var+1))q;d" /home/sourav/EVD-Expt/hashPower)
	# echo "hashPower $hashPowerVar"
	#echo "new hashpower calculated is "

	# if [ $var -le 6 ]; then
	# 	cacheVar=4096
	# elif [ $var -le 13 ]; then
	# 	cacheVar=$((4096*4))
	# elif [ $var -le 20 ]; then
	# 	cacheVar=$((4096*2))
	# elif [ $var -le 27 ]; then
	# 	cacheVar=$((4096*4))
	# elif [ $var -le 34 ]; then
	# 	cacheVar=$((4096*2))
	# elif [ $var -le 41 ]; then
	# 	cacheVar=$((4096*2))
	# fi
	
	# echo "var $var, cache $cacheVar"

	# to run EVD-Prototype
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "
	# 	nohup killall geth; 
	# 	sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/chaindata/; 
	# 	sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/lightchaindata/; 
	# 	sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/nodes/;
	# 	sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/ethash/;
	# 	sudo rm /home/ubuntu/gitRepoEVD/.ethereum/geth/LOCK;
	# 	sudo rm /home/ubuntu/gitRepoEVD/.ethereum/geth/transactions.rlp;
	# 	nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --k 10 init /home/ubuntu/gitRepoEVD/genesis.json; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --rpc --rpcport 22000 --port 21000 --verbosity 3 --gcmode archive --hashpower $hashPowerVar --k 10 --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt" > /home/sourav/EVD-Expt/Logs/log$var.txt 2>&1 &

	# to run go-ethereum
	nohup ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "
		sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/chaindata/; 
		sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/lightchaindata/; 
		sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/nodes/;
		sudo rm -r /home/ubuntu/gitRepoEVD/.ethereum/geth/ethash/;
		sudo rm /home/ubuntu/gitRepoEVD/.ethereum/geth/LOCK;
		sudo rm /home/ubuntu/gitRepoEVD/.ethereum/geth/transactions.rlp;
		nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --rpc --rpcport 22000 --port 21000 --nodiscover --interarrival 15 --k 7 --verbosity 4 --gcmode archive --cache $cacheVar --hashpower $hashPowerVar --behavior $behavior --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt > /home/ubuntu/gitRepoEVD/log.txt 2>&1" &
	
	cacheVar=2048
	behavior=0
	#echo "after starting ************ "$REMOTE_SERVER
	#sleep 2s
	# ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "killall geth; nohup geth --datadir /home/ubuntu/gitRepoEVD/.ethereum --rpc --rpcport 22001 --port 21000 --verbosity 4 --gcmode archive --hashpower 7.1 --k 10 --allow-insecure-unlock --unlock 0 --password /home/ubuntu/gitRepoEVD/passwords.txt" > log$var.txt 2>&1 &
	# echo "after start************ "$REMOTE_SERVER
	var=$((var+1))
	#echo $var
done < $SERVER_LIST
