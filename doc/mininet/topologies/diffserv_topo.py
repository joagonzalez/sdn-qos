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
from mininet.cli import CLI
from mininet.link import Intf

from os import system

import json
from  time import sleep
from api import ApiService

def qosSetup():
    baseUrl = 'http://127.0.0.1:8080'
    datapath = '0000000000000001'
    api = ApiService(baseUrl)

    # Put db address
    ovsdbEndpoint = '/v1.0/conf/switches/' + datapath + '/ovsdb_addr'
    ovsdbData = "tcp:127.0.0.1:6632"
    api.put(ovsdbEndpoint, ovsdbData)
    sleep(1)

    # Post Queue
    queueEndpoint = '/qos/queue/' + datapath
    queueData = {
        "port_name": "s1-eth1",
        "type": "linux-htb",
        "max_rate": "1000000",
        "queues": [{"max_rate": "1000000"},
                   {"max_rate": "200000"},
                   {"min_rate": "500000"}]
    }
    api.post(queueEndpoint, queueData)

    # Post Qos Rule
    ruleEndpoint = '/qos/rules/' + datapath
    ruleData = {"match": {"ip_dscp": "26"},
                "actions": {"queue": "1"}}
    api.post(ruleEndpoint, ruleData)

    # Post Mark Rule
    markEndpoint = '/qos/rules/' + datapath
    markData = {"match": {"nw_dst": "10.0.0.1",
                      "nw_proto": "UDP",
                      "tp_dst": "5002"},
                "actions": {"mark": "26"}}
    api.post(markEndpoint, markData)


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
    c0 = net.get( 'c0' )
    s1 = net.get( 's1' )
    s2 = net.get( 's2' )

    # Iniciar controlador
    info('*** Iniciando ryu...')
    c0.cmd( 'ryu-manager ryu.app.rest_qos ryu.app.qos_simple_switch_13 ryu.app.rest_conf_switch &' )
    sleep(5)

    # Configurar protocolo y manager
    s1.cmd( 'ovs-vsctl set Bridge s1 protocols=OpenFlow13' )
    s2.cmd( 'ovs-vsctl set Bridge s2 protocols=OpenFlow13' )
    s1.cmd( 'ovs-vsctl set-manager ptcp:6632' )

    # Configurar QoS
    info( '*** Configurando ovsdb...' )
    qosSetup() 
    
    CLI( net )
    net.stop()
    
    # Destrouir qos y colas
    system( 'ovs-vsctl --all destroy qos -- --all destroy queue' )

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
