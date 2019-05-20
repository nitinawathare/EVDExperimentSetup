#!/bin/bash

cd gitRepoEVD
sudo rm -r .ethereum
mkdir .ethereum

geth --datadir .ethereum/ 2>> .ethereum/setup.log &
sleep 3s

IPAddress="$(ifconfig eth0| grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')"
echo $IPAddress
#192.168.1.25


echo "[\"$(cat .ethereum/setup.log | grep -oEi '(enode.*@)'| head -1)"${IPAddress}":21000?discport=0&raftport=23000\"]" >> .ethereum/static-nodes.json
killall geth
sudo rm -r .ethereum/geth

geth --datadir .ethereum --password passwords.txt account new

cd ..

