#!/bin/bash

cd gitRepoEVD
sudo rm -r .ethereum
mkdir .ethereum

geth --datadir .ethereum/ 2>> .ethereum/setup.log &
sleep 3s
echo "[\"$(cat .ethereum/setup.log | grep -oEi '(enode.*@)'| head -1)192.168.1.3:21000?discport=0&raftport=23000\"]" >> .ethereum/static-nodes.json
killall geth
sudo rm -r .ethereum/geth

geth --datadir .ethereum --password passwords.txt account new

cd ..
