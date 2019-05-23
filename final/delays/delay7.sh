#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 51.514ms --dst-network 129.154.96.64
sudo tcset eth0 --add --delay 230.19ms --dst-network 129.154.96.71
