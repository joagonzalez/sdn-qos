https://osrg.github.io/ryu-book/en/html/rest_qos.html https://osrg.github.io/ryu-book/en/html/rest_qos.html#rest-api-list - API REST QoS (rest_qos)

# GET commands QoS
switch = 0000000000000001 curl -X GET http://localhost:8080/qos/queue/status/{switch} - queue status curl -X GET http://localhost:8080/qos/queue/{switch} - queue configuration curl -X GET http://localhost:8080/qos/queue/{switch} - queue configuration curl -X GET http://localhost:8080/qos/rules/{switch} - QoS rules curl -X GET http://localhost:8080/qos/meter/{switch} - Meter statistics

# Test Labo QoS flujo en puerto 5002 UDP con cola de 800Kbps Min rate
curl -X POST -d '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "500000"}, {"min_rate": "800000"}]}' http://localhost:8080/qos/queue/0000000000000001 curl -X POST -d '{"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001

# Test labo QoS
curl -X POST -d '{"match": {"ip_dscp": "0", "in_port": "2"}, "actions":{"queue": "1"}}' http://10.10.10.120:8080/qos/rules/0000000000000001 curl -X POST -d '{"match": {"ip_dscp": "10", "in_port": "2"}, "actions":{"queue": "3"}}' http://10.10.10.120:8080/qos/rules/0000000000000001 curl -X POST -d '{"match": {"ip_dscp": "12", "in_port": "2"}, "actions":{"queue": "2"}}' http://10.10.10.120:8080/qos/rules/0000000000000001 curl -X POST -d '{"match": {"ip_dscp": "0", "in_port": "3"}, "actions":{"queue": "1"}}' http://10.10.10.120:8080/qos/rules/0000000000000001 curl -X POST -d '{"match": {"ip_dscp": "10", "in_port": "3"}, "actions":{"queue": "3"}}' http://10.10.10.120:8080/qos/rules/0000000000000001 curl -X POST -d '{"match": {"ip_dscp": "12", "in_port": "3"}, "actions":{"queue": "2"}}' http://10.10.10.120:8080/qos/rules/0000000000000001

# Caso 1
Try to measure the bandwidth by using iperf. h1(server) is listening on port 5001 and 5002 and port 5003 in the UDP protocol. h2, h3 (client) sends the traffic of each class addressed to h1.

# h1
iperf -s -u -p 5001 & iperf -s -u -p 5002 & iperf -s -u -p 5003 &

# h2
iperf -c 10.0.0.1 -p 5001 -u -b 800K

# Caso 2
Best-effort traffic & AF11 excess traffic

# h2
iperf -c 10.0.0.1 -p 5001 -u -b 800K

# h3
iperf -c 10.0.0.1 -p 5002 -u -b 600K --tos 0x28