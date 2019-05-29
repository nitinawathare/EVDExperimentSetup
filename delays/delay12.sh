#!/bin/bash
wget https://github.com/thombashi/tcconfig/releases/download/v0.19.0/tcconfig_0.19.0_amd64.deb
sudo dpkg -i tcconfig_0.19.0_amd64.deb
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 103.349ms --dst-network 129.154.120.163
sudo tcset eth0 --add --delay 103.349ms --dst-network 129.154.127.149
sudo tcset eth0 --add --delay 175.195ms --dst-network 129.154.121.21
sudo tcset eth0 --add --delay 56.549ms --dst-network 129.154.121.209
sudo tcset eth0 --add --delay 29.749ms --dst-network 129.154.120.26
