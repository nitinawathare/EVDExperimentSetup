#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 154.23ms --dst-network 129.154.121.209
sudo tcset eth0 --add --delay 80.557ms --dst-network 129.154.96.71
sudo tcset eth0 --add --delay 154.23ms --dst-network 129.154.120.134
