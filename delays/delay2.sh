#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 0.4ms --dst-network 129.154.105.232
sudo tcset eth0 --add --delay 80.557ms --dst-network 129.154.127.47
sudo tcset eth0 --add --delay 263.221ms --dst-network 129.154.96.115
sudo tcset eth0 --add --delay 306.415ms --dst-network 129.154.127.104
sudo tcset eth0 --add --delay 345.005ms --dst-network 129.154.120.26
