#!/bin/bash

cd gitRepoEVD

ssh-add
ssh-add -l
eval `ssh-agent -s`
git clone git+ssh://git@github.com/sourav1547/EVD-Prototype.git

cd EVD-Prototype
git checkout origin/evd1
make clean
#echo "making code************************************"
make
#echo "END making code************************************"

sudo cp build/bin/geth /usr/local/bin
cd ..

cd ..
