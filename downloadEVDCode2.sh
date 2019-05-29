#!/bin/bash

cd gitRepoEVD
cd EVD-Prototype
git checkout evd2
git pull origin evd2

make clean
#echo "making code************************************"
make
#echo "END making code************************************"
killall geth
sudo cp build/bin/geth /usr/local/bin
cd ../..
