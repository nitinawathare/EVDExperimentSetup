#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 64.024ms --dst-network 129.154.121.209
sudo tcset eth0 --add --delay 26.163ms --dst-network 129.154.96.64
sudo tcset eth0 --add --delay 49.28ms --dst-network 129.154.96.115
sudo tcset eth0 --add --delay 49.28ms --dst-network 129.154.121.18
sudo tcset eth0 --add --delay 90.204ms --dst-network 129.154.106.127
