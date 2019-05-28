#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 64.024ms --dst-network 129.154.96.116
