#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 28.097ms --dst-network 129.154.96.115
sudo tcset eth0 --add --delay 51.514ms --dst-network 129.154.121.209
sudo tcset eth0 --add --delay 51.514ms --dst-network 129.154.120.134
