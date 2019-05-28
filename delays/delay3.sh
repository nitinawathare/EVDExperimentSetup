#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 73.305ms --dst-network 129.154.96.64
sudo tcset eth0 --add --delay 154.23ms --dst-network 129.154.105.174
