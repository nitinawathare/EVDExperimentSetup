#!/bin/bash

killall geth

cd gitRepoEVD

sudo rm -r .ethereum
sudo rm -r .ethereum1

mkdir .ethereum
mkdir .ethereum1


IPAddress="$(ifconfig eth0| grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')"
echo $IPAddress

nohup geth --datadir .ethereum/ 2>> .ethereum/setup.log &
sleep 3s
echo "[\"$(cat .ethereum/setup.log | grep -oEi '(enode.*@)'| head -1)"${IPAddress}":21000?discport=0&raftport=23000\"]" >> .ethereum/static-nodes.json

killall geth

nohup geth --datadir .ethereum1/ 2>> .ethereum1/setup.log &

sleep 3s

echo "[\"$(cat .ethereum1/setup.log | grep -oEi '(enode.*@)'| head -1)"${IPAddress}":21001?discport=0&raftport=23001\"]" >> .ethereum1/static-nodes.json


killall geth
sudo rm -r .ethereum/geth/chaindata/ #.ethereum/geth/chaindata/
sudo rm -r .ethereum1/geth/chaindata/

geth --datadir .ethereum --password passwords.txt account new
geth --datadir .ethereum1 --password passwords.txt account new

cd ..

