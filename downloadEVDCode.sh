#!/bin/bash

cd gitRepoEVD

sudo rm -r EVD-Prototype

ssh-keyscan -H github.com >> ~/.ssh/known_hosts

ssh-add
ssh-add -l
eval `ssh-agent -s`
git clone git+ssh://git@github.com/sourav1547/EVD-Prototype.git

cd EVD-Prototype

git checkout origin/evd2

make clean
#echo "making code************************************"
make
#echo "END making code************************************"
killall geth
sudo cp build/bin/geth /usr/local/bin
cd ../..
