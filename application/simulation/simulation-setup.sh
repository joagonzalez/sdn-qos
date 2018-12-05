#!/usr/bin/env bash
./wait-for-it.sh asterisk:8088 -s -t 0
./wait-for-it.sh ryu:8080 -s -t 0
./wait-for-it.sh call_admission_control_backend:8000 -s -t 0

# Sends TCPDUMP output from network eth0 interface and sends to cac_backend to port 9999 with netcat
# a este tcpdump hay que hacerle algo con sed | awk para filtrar la info necesaria
#tcpdump -i eth0 | nc 172.18.0.13 9999 &
# Correr en background para que continue ejecutando a sip sino se queda buferendo en el proceso principal
# Esta es la red que hay que escuchaR? me parece que es la de mininet, no?

# Simulator
sipp -d 10000 -s 7000 172.18.0.11 -l 5 -mp 5606

# Ahora pasa algo con el sipp que tira error y no se conecta en el asterisk cuando queire hacer la llamada obviamente
