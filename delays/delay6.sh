#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 26.163ms --dst-network 129.154.96.64
sudo tcset eth0 --add --delay 331.685ms --dst-network 129.154.96.71
sudo tcset eth0 --add --delay 64.024ms --dst-network 129.154.105.174
