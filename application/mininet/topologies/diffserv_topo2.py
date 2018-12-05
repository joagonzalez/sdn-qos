'''
h1 --- s1 --- s2 ---h2

queues    min_rate    max_rate
    0       ---        1000000
    1       ---        200000
    2      500000        ---
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Controller, RemoteController
from mininet.log import setLogLevel, info
import logging
import os
from mininet.cli import CLI
from mininet.link import Intf

import json
from  time import sleep
from api import ApiService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

def iperfTest(h1, h2):
    logger.debug("Start iperfTEST")
    
    #wireshark
    h1.cmdPrint('wireshark &')

    #iperf Server
    h1.cmdPrint('iperf -s -u -p 5001 -i 1 > results5001 &')
    h1.cmdPrint('iperf -s -u -p 5002 -i 1 > results5002 &')
    #iperf Clients
    t = 50
    h2.cmdPrint('iperf -c ' + h1.IP() + ' -u -t ' + str(t) + ' -i 1 -p 5001 -b 1M &')
    h2.cmdPrint('iperf -c ' + h1.IP() + ' -u -t ' + str(t) + ' -i 1 -p 5002 -b 1M &')
    sleep(t)
    h1.cmdPrint('killall -9 iperf')

    #process results
    h1.cmdPrint("cat results5001 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5001")
    h1.cmdPrint("cat results5002 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5002")

def pingTest(net):
    logger.debug("Start Test all network")
    net.pingAll()

def qosSetup():
    baseUrl = 'http://0.0.0.0:8080'
    datapath = '0000000000000001'
    api = ApiService(baseUrl)

    # Put db address
    ovsdbEndpoint = '/v1.0/conf/switches/' + datapath + '/ovsdb_addr'
    ovsdbData = "tcp:127.0.0.1:6632"
    api.put(ovsdbEndpoint, ovsdbData)
    sleep(2)

    # Post Queue
    queueEndpoint = '/qos/queue/' + datapath
    queueData = {
        "port_name": "s1-eth1",
        "type": "linux-htb",
        "max_rate": "1000000",
        "queues": [{"max_rate": "100000"},
                   {"max_rate": "500000"},
                   {"min_rate": "800000"}]
    }
    api.post(queueEndpoint, queueData)

    # Post Qos Rule
    ruleEndpoint = '/qos/rules/' + datapath
    #ruleData = {"match": {"ip_dscp": "26"},
    #            "actions": {"queue": "1"}}
    
    ruleData1 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5001"}, "actions":{"queue": "0"}}
    ruleData2 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "1"}}
    
    api.post(ruleEndpoint, ruleData1)
    api.post(ruleEndpoint, ruleData2)

    # Post Mark Rule
    #markEndpoint = '/qos/rules/' + datapath
    # markData = {"match": {"nw_dst": "10.0.0.1",
    #                  "nw_proto": "UDP",
    #                  "tp_dst": "5002"},
    #            "actions": {"mark": "26"}}
    #api.post(markEndpoint, markData)


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
    net = Mininet( topo=topo, controller=RemoteController, autoSetMacs=True )
    net.start()

    # Get nodes
    s1 = net.get( 's1' )
    s2 = net.get( 's2' )
    h1 = net.get('h1')
    h2 = net.get('h2')

    # Iniciar controlador
    info('*** Iniciando ryu...')
    try:
        info('por ahora no ejecutamos ryu aca...')
        #os.system('ryu-manager  ryu.app.qos_simple_switch_13_CAC ryu.app.qos_simple_switch_rest_13_CAC ryu.app.rest_conf_switch ryu.app.rest_qos &')
    except ValueError:
        info('Error...')

    sleep(3)

    # Configurar protocolo y manager
    info('*** Configurando OpenFlow13 en s1')
    s1.cmd( 'ovs-vsctl set Bridge s1 protocols=OpenFlow13' )
    info('*** Configurando OpenFlow13 en s2')
    s2.cmd( 'ovs-vsctl set Bridge s2 protocols=OpenFlow13' )
    info('*** Configurando OVSDB port') 
    s1.cmd( 'ovs-vsctl set-manager ptcp:6632' )
    s2.cmd( 'ovs-vsctl set-manager ptcp:6632' )

    # Configurar QoS
    info( '*** Configurando QoS...' )
    try:
        qosSetup() 
        sleep(2)
    except ValueError:
        print('Error....')

    # Ejecutamos pruebas
    iperfTest(h1, h2)


    CLI( net )
    net.stop()
    
    # Destruir qos y colas
    info('*** Delete qos and queues in s1 and s2...')
    s1.cmdPrint('ovs-vsctl --all destroy QoS')
    s1.cmdPrint('ovs-vsctl --all destroy queue')
    sleep(2)
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
