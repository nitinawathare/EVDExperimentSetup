#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 29.749ms --dst-network 129.154.96.115
sudo tcset eth0 --add --delay 27.402ms --dst-network 129.154.101.242
sudo tcset eth0 --add --delay 0.4ms --dst-network 129.154.106.131
