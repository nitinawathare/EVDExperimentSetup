#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 0.4ms --dst-network 129.154.96.71
