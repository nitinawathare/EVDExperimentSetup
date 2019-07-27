#!/bin/bash

cd gitRepoEVD

sudo rm -r EVD-go-ethereum

ssh-keyscan -H github.com >> ~/.ssh/known_hosts

ssh-add
ssh-add -l
eval `ssh-agent -s`
git clone git+ssh://git@github.com/sourav1547/EVD-go-ethereum.git

cd EVD-go-ethereum

git checkout origin/skip2

make clean
#echo "making code************************************"
make
#echo "END making code************************************"
killall geth
sudo cp build/bin/geth /usr/local/bin
cd ../..
