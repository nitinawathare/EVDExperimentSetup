#!/bin/bash
sudo tc qdisc del dev eth0 root
sudo tcset eth0 --add --delay 331.685ms --dst-network 129.154.96.72
