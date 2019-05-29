#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 49.28ms --dst-network 129.154.96.115
sudo tcset eth0 --add --delay 39.043ms --dst-network 129.154.127.104
