#####################################
### CAC Simulation Mininet Script ###
#####################################

#####################################
###         CAC Topology          ###
#####################################'''
'''
               |--(s1-eth1) s1 (s1-eth2)---(s2-eth2) s2 (s2-eth1)--|
h1 (h1-eth0)---|                                                   |---(h12eth0) h2

queues    min_rate    max_rate
    0      200000      ---  
    1      300000      ---  
    2       ---        800000
'''

# Mininet modules
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf
# Python external modules
import json
import logging
import os
from  time import sleep
from topologies.api import ApiService

# logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

### Settings

# QoS settings methods
def switch_query(switch):
    datapath = '000000000000000' + str(switch)
  
    return datapath

def controller_query(ip, port):
    controllerUrl = 'http://' + ip + ':' + port

    return controllerUrl

def configureOVSdb(switches):
    i = 1
    for switch in switches:
        s = 's' + str(i)
        info('*** Configurando OpenFlow13 en ' + s)
        switch.cmd( 'ovs-vsctl set Bridge ' + s + ' protocols=OpenFlow13' )
        info('*** Configurando OVSDB port') 
        switch.cmd( 'ovs-vsctl set-manager ptcp:6632' )
        i = i + 1

def deleteQoS(switches):
    info('*** Delete qos and queues...')
    for switch in switches:
        switch.cmdPrint('ovs-vsctl --all destroy QoS')
        switch.cmdPrint('ovs-vsctl --all destroy queue')

# DSCP/ToS tagging
def dscp_mark(switch, controllerUrl):
    datapath = switch_query(switch)
    api = ApiService(controllerUrl)

    # Mark Rules
    markEndpoint = '/qos/rules/' + datapath
    markData1 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5001"}, "actions": {"mark": "26"}}
    markData2 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions": {"mark": "10"}}
    markData3 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5003"}, "actions": {"mark": "12"}}
    # API queries
    api.post(markEndpoint, markData1)
    api.post(markEndpoint, markData2)
    api.post(markEndpoint, markData3)

# iperfTest simulate best effort traffic between hosts
def iperfTest(hosts, testPorts, time):
    logger.debug("Start iperfTEST")
    server = hosts[0]
    client = hosts[1]

    for port in testPorts:
    #iperf Server
        server.cmdPrint('iperf -s -u -p ' + str(port) + ' -i 1 > results' + str(port) + ' &')

    for port in testPorts:
    #iperf Clients
        client.cmdPrint('iperf -c ' + server.IP() + ' -u -t ' + str(time) + ' -i 1 -p ' + str(port) + ' -b 1M &')
    
    sleep(time)
    client.cmdPrint('killall -9 iperf')
    server.cmdPrint('killall -9 iperf')

def processIperfResults():
    #process results
    #h1.cmdPrint("cat results5001 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5001")
    #h1.cmdPrint("cat results5002 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5002")
    #h1.cmdPrint("cat results5002 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5003")
    sleep(1)

def pingTest(net):
    logger.debug("Start Test all network")
    net.pingAll()

def qosSetup(test, switch, controllerUrl):
    # poner en otra funcion
    datapath = switch_query(switch)
    api = ApiService(controllerUrl)

    # Put db address (poner en otra fucion)
    ovsdbEndpoint = '/v1.0/conf/switches/' + datapath + '/ovsdb_addr'
    ovsdbData = "tcp:127.0.0.1:6632"
    api.put(ovsdbEndpoint, ovsdbData)
    sleep(2)


    # Post Queue
    if test == 1:
        queueEndpoint = '/qos/queue/' + datapath
        queueData = {
            "port_name": "s" + str(switch) + "-eth1",
            "type": "linux-htb",
            "max_rate": "1000000",
            "queues": [{"max_rate": "100000"},
                    {"max_rate": "200000"},
                    {"max_rate": "300000"},
                    {"min_rate": "800000"}]
        }

        api.post(queueEndpoint, queueData)
    else:
        queueEndpoint = '/qos/queue/' + datapath
        queueData = {
            "port_name": "s" + str(switch) + "-eth1",
            "type": "linux-htb",
            "max_rate": "1000000",
            "queues": [{"max_rate": "200000"},
                    {"max_rate": "300000"},
                    {"max_rate": "100000"},
                    {"min_rate": "800000"}]
        }
        api.post(queueEndpoint, queueData)

    # Post Qos Rule - La mejora seria colorear paquetes y luego asignar colas en base a marcas y no puertos
    # tambien habra que repensar cuando tengamos el puerto desde ari de las llamadas
    ruleEndpoint = '/qos/rules/' + datapath
    #ruleData = {"match": {"ip_dscp": "26"},
    #            "actions": {"queue": "1"}}
    
    ruleData1 = {"match": {"ip_dscp": "26"}, "actions":{"queue": "0"}}
    ruleData2 = {"match": {"ip_dscp": "10"}, "actions":{"queue": "1"}}
    ruleData3 = {"match": {"ip_dscp": "12"}, "actions":{"queue": "2"}}
    
    api.post(ruleEndpoint, ruleData1)
    api.post(ruleEndpoint, ruleData2)
    api.post(ruleEndpoint, ruleData3)

class MyTopo( Topo ):
    "Test topology"

    def build( self, **opts ):

        # add switches
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )

        # add hosts
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        
        self.addLink( h1, s1 )
        self.addLink( h2, s2 )
        self.addLink( s1, s2 )


def run():

    topo = MyTopo()
    # Defining remote controller (Ryu)
    controller = RemoteController( 'c0', ip='127.0.0.1', port=6633 )
    net = Mininet( topo=topo, controller=controller, autoSetMacs=True )
    net.start()

    # Enviroment settings
    controllerUrl = controller_query('0.0.0.0', '8080')

    # Get nodes - could be built with for in the future
    [s1, s2] = [net.get('s1'), net.get('s2')]
    [h1, h2] = [net.get('h1'), net.get('h2')]
    switches = [s1, s2]    
    hosts = [h1, h2]
    ports = ['5001', '5002', '5003']
    time = 20
    sleep(3)

    # Configurar protocolo y manager - could be a method
    configureOVSdb(switches)
    sleep(2)

    # wireshark
    h1.cmdPrint('wireshark &')
    sleep(5)

    # Configurar QoS and test execution
    info( '*** Configurando DSCP tags...' )
    dscp_mark(2, controllerUrl)   
    info( '*** Configuring QoS first wave...' )
    qosSetup(1, 1, controllerUrl) # (test, switch, controllerUrl)
    iperfTest(hosts, ports, time)
    
    info( '*** Configurando DSCP tags...' )
    dscp_mark(2, controllerUrl)
    info( '*** Configuring QoS second wave...' )
    qosSetup(2, 1, controllerUrl)
    iperfTest(hosts, ports, time)
    
    info( '*** Configurando DSCP tags...' )
    dscp_mark(2, controllerUrl)
    info( '*** Configuring QoS third wave...' )
    qosSetup(1, 1, controllerUrl)
    iperfTest(hosts, ports, time)

    # Open Mininet CLI 
    CLI( net )

    net.stop()

    # Destruir qos y colas
    deleteQoS(switches)
    sleep(2)    
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
