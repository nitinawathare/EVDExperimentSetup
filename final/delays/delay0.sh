#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 27.402ms --dst-network 129.154.102.125
sudo tcset eth0 --add --delay 345.005ms --dst-network 129.154.102.222
sudo tcset eth0 --add --delay 27.402ms --dst-network 129.154.103.120