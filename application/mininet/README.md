# Mininet 
Service that enable a fast way to test network scenarios with ryu and custom sdn application

### Real Time QoS
Script *sdn-qos-RealTimeQueues.py* implement an automated test where packet prioritization could be achieve using ryu controller with mininet and ovs.

**Mininet**
```bash
sudo python2.7 sdn-qos-RealTimeQueues.py 
```

**Ryu**
```
python3 ryu-manager ryu.app.rest_qos ryu.app.qos_simple_switch_13 ryu.app.rest_conf_switch
```