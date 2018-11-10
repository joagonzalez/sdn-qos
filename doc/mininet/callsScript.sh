#!/usr/bin/env bash

$ip_asterisk=10.10.10.106

sudo docker attach mininet

#Register endpoint Alice (evaluate if ssh its a better approach)
xterm h1
linphonec
register alice@$ip_asterisk 1234


#Register endpoint Bob
xterm h2
linephonec
register bob@$ip_asterisk 4321 
#Generating Calls
call 7000
call 7000

