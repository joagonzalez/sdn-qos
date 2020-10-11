# newcos-polling
![Python](https://img.shields.io/badge/mininet-v2.1.1-orange)
![Python](https://img.shields.io/badge/ryuframework-4.34-blue)
![Python](https://img.shields.io/badge/python-v2.7-blue)
![Python](https://img.shields.io/badge/python-v3.6-blue)
![Python](https://img.shields.io/badge/platform-linux--64%7Cwin--64-lightgrey)

# Mininet 
Service that enables a fast way to test network scenarios with ryu and custom sdn application. Not neccesary when application is used in production environments.

## Real Time QoS
Script *sdn-qos-RealTimeQueues.py* implement an automated test where packet prioritization could be achieve using ryu controller with mininet and ovs.

**Mininet**
```bash
sudo python2.7 sdn-qos-RealTimeQueues.py 
```

**Ryu**
```
workon ryu
python3 ./bin/ryu-manager --observe-links ryu.app.rest_topology ryu.app.ws_topology ryu.app.ofctl_rest ryu.app.qos_simple_switch_13_CAC ryu.app.qos_simple_switch_rest_13_CAC ryu.app.rest_conf_switch ryu.app.rest_qos ryu.app.gui_topology.gui_topology
```