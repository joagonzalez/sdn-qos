curl -X GET http://localhost:8080/qos/queue/status/0000000000000001
curl -X GET http://localhost:8080/qos/queue/status/0000000000000002
curl -X GET http://localhost:8080/qos/rules/0000000000000001
curl -X GET http://localhost:8080/qos/rules/0000000000000002

curl -X GET http://localhost:8080/qos/meter/status/0000000000000001

curl -X DELETE http://localhost:8080/qos/queue/0000000000000001
curl -X DELETE http://localhost:8080/qos/queue/0000000000000002
curl -X DELETE -d '{"qos_id":"all"}' http://localhost:8080/qos/rules/0000000000000001
curl -X DELETE -d '{"qos_id":"all"}' http://localhost:8080/qos/rules/0000000000000002


curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr
curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000002/ovsdb_addr


### QoS
curl -X POST -d '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "500000"}, {"min_rate": "800000"}]}' http://localhost:8080/qos/queue/0000000000000001 
curl -X POST -d '{"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "1"}}' http://localhost:8080/qos/rules/0000000000000001


# Caso 1
Try to measure the bandwidth by using iperf. h1(server) is listening on port 5001 and 5002 and port 5003 in the UDP protocol. h2, h3 (client) sends the traffic of each class addressed to h1.

#h1> iperf -s -u -p 5001 -i 1
#h1> iperf -s -u -p 5002 -i 1
#h2> iperf -c 10.0.0.1 -p 5001 -u -b 100M -t 200
#h2> iperf -c 10.0.0.1 -p 5001 -u -b 100M -t 200
