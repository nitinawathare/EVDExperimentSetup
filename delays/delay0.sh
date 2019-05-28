#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 345.005ms --dst-network 129.154.96.71
sudo tcset eth0 --add --delay 27.402ms --dst-network 129.154.103.120
sudo tcset eth0 --add --delay 27.402ms --dst-network 129.154.101.242
sudo tcset eth0 --add --delay 49.476ms --dst-network 129.154.105.174
