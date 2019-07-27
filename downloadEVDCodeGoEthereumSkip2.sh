#!/bin/bash

cd gitRepoEVD
cd EVD-go-ethereum
git checkout skip2
git pull origin skip2

make clean
#echo "making code************************************"
make
#echo "END making code************************************"
killall geth
sudo cp build/bin/geth /usr/local/bin
cd ../..
