
#!/bin/bash
SERVER_LIST=ipList

folder=$(date +%d-%m-%Y-%H-%M-%S)		
folderEr=EC$(date +%d-%m-%Y-%H-%M-%S)
var=0

if [ "$1" = "genesis" ]; then
	echo "Received $1 Command"

elif [ "$1" = "contAdd" ]; then
	echo "Received $1 Command"

elif [ "$1" = "contGen" ]; then
	echo "Received $1 Command"

elif [ "$1" = "contMem" ]; then
	echo "Received $1 Command"

elif [ "$1" = "pyScripts" ]; then
	echo "Received $1 Command"

elif [ "$1" = 'reset' ]; then
	echo "Received $1 Command"

elif [ "$1" = "copyDataEth" ]; then
	mkdir /home/sourav/EVD-Data/$folder
	mkdir /home/sourav/EVD-Data/$folder/Mi
	mkdir /home/sourav/EVD-Data/$folder/Mc
	mkdir /home/sourav/EVD-Data/$folder/Log
	mkdir /home/sourav/EVD-Data/$folder/Ex
	mkdir /home/sourav/EVD-Data/$folder/Ti

elif [ "$1" = "copyData" ]; then
	mkdir /home/sourav/EVD-Data/$folder
	mkdir /home/sourav/EVD-Data/$folder/Mi
	mkdir /home/sourav/EVD-Data/$folder/Mc
	mkdir /home/sourav/EVD-Data/$folder/Log
	mkdir /home/sourav/EVD-Data/$folder/Ex
	mkdir /home/sourav/EVD-Data/$folder/Ti
	mkdir /home/sourav/EVD-Data/$folder/Ql
	mkdir /home/sourav/EVD-Data/$folder/PPt

elif [ "$1" = "copyErr" ]; then
	mkdir /home/sourav/EVD-Data/$folderEr
	mkdir /home/sourav/EVD-Data/$folderEr/Mi
	mkdir /home/sourav/EVD-Data/$folderEr/Mc
	mkdir /home/sourav/EVD-Data/$folderEr/Log
	mkdir /home/sourav/EVD-Data/$folderEr/Ex
	mkdir /home/sourav/EVD-Data/$folderEr/Ti
	mkdir /home/sourav/EVD-Data/$folderEr/Ql
	mkdir /home/sourav/EVD-Data/$folderEr/PPt
else
	echo "
	'copyErr'		to copy data in Error Folder
	'copyData'		to copy data in Data folder
	'copyDataEth		to copy data of Go-Ethereum run in Data folder
	'reset'			to reset Remote 
	'genesis' 		to copy genesis
	'contAdd'		to copy contractAddressList
	'contGen'		to copy General contracts
	'contMem'		to copy Memory based contracts
	'pyScripts'		to copy sendTransaction, deployContract etc.
	"
fi


while read REMOTE_SERVER
do
	 #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "sudo rm -r gitRepoEVD" 
	 #ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "mkdir gitRepoEVD" 
 	#scp -i quorum2.key addressRead.py staticJsonRead.py staticJsonRead1.py passwords.txt installGo.sh downloadEVDCode.sh downloadEVDCode2.sh setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&

	# mkdir ~/VMQuorumNode/Node$REMOTE_SERVER
	# ssh -o StrictHostKeyChecking=no -l sourav $REMOTE_SERVER&

	if [ "$1" = "genesis" ]; then
		scp -i quorum2.key genesis.json ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&

	elif [ "$1" = "contAdd" ]; then
		scp -i quorum2.key contractAddressList ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/&

	elif [ "$1" = "contGen" ]; then
		scp -i quorum2.key matrixMultiplication.sol cpuheavy.sol emptyLoop.sol ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &

	elif [ "$1" = "contMem" ]; then
		scp -i quorum2.key matrixMemory.sol sortMemory.sol emptyLoop.sol ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &

	elif [ "$1" = "pyScripts" ]; then
		scp -i quorum2.key sendTransaction.py deployContract.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
		scp -i quorum2.key sendEVDTransaction.py deployEVDContract.py ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
		
	elif [ "$1" = "reset" ]; then
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/queuLengthStats" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/processPreviousTime" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/miningInfo" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/minersInChain" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/log.txt" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/executionTime" &
		ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "> /home/ubuntu/gitRepoEVD/experimentTimeStats" &

	elif [ "$1" = "copyErr" ]; then
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/miningInfo /home/sourav/EVD-Data/$folderEr/Mi/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/minersInChain /home/sourav/EVD-Data/$folderEr/Mc/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/log.txt /home/sourav/EVD-Data/$folderEr/Log/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/executionTime /home/sourav/EVD-Data/$folderEr/Ex/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/experimentTimeStats /home/sourav/EVD-Data/$folderEr/Ti/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/queuLengthStats /home/sourav/EVD-Data/$folderEr/Ql/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/processPreviousTime /home/sourav/EVD-Data/$folderEr/PPt/$var.dat & 

	elif [ "$1" = "copyDataEth" ]; then 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/miningInfo /home/sourav/EVD-Data/$folder/Mi/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/minersInChain /home/sourav/EVD-Data/$folder/Mc/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/log.txt /home/sourav/EVD-Data/$folder/Log/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/executionTime /home/sourav/EVD-Data/$folder/Ex/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/experimentTimeStats /home/sourav/EVD-Data/$folder/Ti/$var.txt &

	elif [ "$1" = "copyData" ]; then 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/miningInfo /home/sourav/EVD-Data/$folder/Mi/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/minersInChain /home/sourav/EVD-Data/$folder/Mc/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/log.txt /home/sourav/EVD-Data/$folder/Log/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/executionTime /home/sourav/EVD-Data/$folder/Ex/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/experimentTimeStats /home/sourav/EVD-Data/$folder/Ti/$var.txt & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/queuLengthStats /home/sourav/EVD-Data/$folder/Ql/$var.dat & 
		scp -r -i quorum2.key ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/processPreviousTime /home/sourav/EVD-Data/$folder/PPt/$var.dat &
	else
		break
	fi

	#scp -i quorum2.key installpy3.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/ &
	#scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
    #scp -i quorum2.key installGo.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key downloadEVDCode.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	#scp -i quorum2.key setupEthereum.sh ubuntu@$REMOTE_SERVER:/home/ubuntu/gitRepoEVD/
	 
	#ssh -n -i quorum2.key ubuntu@$REMOTE_SERVER "geth --datadir /home/ubuntu/gitRepoEVD/.ethereum init /home/ubuntu/gitRepoEVD/genesis.json"

	var=$((var+1))
done < $SERVER_LIST