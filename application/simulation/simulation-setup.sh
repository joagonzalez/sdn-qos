#!/usr/bin/env bash
./wait-for-it.sh asterisk:8088 -s -t 0
./wait-for-it.sh ryu:8080 -s -t 0
./wait-for-it.sh call_admission_control_backend:8000 -s -t 0

# Simulator
if [ $SIMULATION == 'v1' ]
then
    sipp -d 20000 -s 7000 172.18.0.11 -l 1 -mp 5606 & sleep 21; kill -9 -INT %+
    sipp -d 20000 -s 7000 172.18.0.11 -l 1 -mp 5606 & sleep 21; kill -9 -INT %+
    sipp -d 20000 -s 7000 172.18.0.11 -l 1 -mp 5606
else
    sipp -d 20000 -s 7000 172.18.0.11 -l 3 -mp 5606
fi

