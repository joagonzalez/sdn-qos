#!/usr/bin/env bash
./wait-for-it.sh asterisk:8088 -s -t 0
./wait-for-it.sh ryu:8080 -s -t 0
./wait-for-it.sh call_admission_control_backend:8000 -s -t 0

# does TCPDUMP and sends to cac-backend 9999 port with netcat
tcpdump -i eth0 | nc 172.18.0.13 9999 &
sipp -d 10000 -s 100 172.18.0.11 -l 5 -mp 5606

# Pasa algo con el sipp que tira error y no se conecta en el asterisk cuando queire hacer la llamada obviamente
