#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 154.23ms --dst-network 129.154.127.143
sudo tcset eth0 --add --delay 85.485ms --dst-network 129.154.120.164
sudo tcset eth0 --add --delay 80.557ms --dst-network 129.154.120.26
