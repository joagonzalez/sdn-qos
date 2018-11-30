#!/usr/bin/env bash
/wait-for-it.sh asterisk:8088 -s -t 0
/wait-for-it.sh ryu:8080 -s  -t 0

service openvswitch-switch start

mn --controller remote,ip=172.18.0.10 --topo=tree,3