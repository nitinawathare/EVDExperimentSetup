#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 0.4ms --dst-network 129.154.96.71
sudo tcset eth0 --add --delay 263.221ms --dst-network 129.154.96.115
sudo tcset eth0 --add --delay 331.685ms --dst-network 129.154.101.242
