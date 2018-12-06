#!/usr/bin/python

"""
Create a network and start sshd(8) on each host.

Wrapping up functionalities in this script:

- creating a convenience function to construct networks
- connecting the host network to the root namespace
- running server processes (sshd in this case) on hosts
- run traffic with iperf between hosts
- deploy queues in order to prioritize traffic

"""

import sys
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg, info
from mininet.node import Node, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.util import waitListening
import logging

import json
from  time import sleep
from api import ApiService

info("\nlogging...")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger( __name__ )

def iperfTest(h1, h2):
    logger.debug("Start iperfTEST")

    #iperf Server
    h1.cmdPrint('iperf -s -u -p 5001 -i 1 > results5001 &')
    h1.cmdPrint('iperf -s -u -p 5002 -i 1 > results5002 &')
    h1.cmdPrint('iperf -s -u -p 5002 -i 1 > results5003 &')

    #iperf Clients
    t = 25
    h2.cmdPrint('iperf -c ' + h1.IP() + ' -u -t ' + str(t) + ' -i 1 -p 5001 -b 1M &')
    h2.cmdPrint('iperf -c ' + h1.IP() + ' -u -t ' + str(t) + ' -i 1 -p 5002 -b 1M &')
    h2.cmdPrint('iperf -c ' + h1.IP() + ' -u -t ' + str(t) + ' -i 1 -p 5003 -b 1M &')
    sleep(t)
    h1.cmdPrint('killall -9 iperf')

    #process results
    h1.cmdPrint("cat results5001 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5001")
    h1.cmdPrint("cat results5002 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5002")
    h1.cmdPrint("cat results5002 | grep sec | head - " + str(t) + ' | tr - " " ' + " | awk '{print $4,$8}' > new_result5003")

def pingTest(net):
    logger.debug("Start Test all network")
    net.pingAll()

def qosSetup(test):
    baseUrl = 'http://ryu-controller:8080'
    datapath = '0000000000000001'
    api = ApiService(baseUrl)

    # Put db address
    ovsdbEndpoint = '/v1.0/conf/switches/' + datapath + '/ovsdb_addr'
    ovsdbData = "tcp:127.0.0.1:6632"
    api.put(ovsdbEndpoint, ovsdbData)
    sleep(2)


    # Post Queue
    if test == 1:
        queueEndpoint = '/qos/queue/' + datapath
        queueData = {
            "port_name": "s1-eth1",
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
            "port_name": "s1-eth1",
            "type": "linux-htb",
            "max_rate": "1000000",
            "queues": [{"max_rate": "200000"},
                    {"max_rate": "300000"},
                    {"max_rate": "100000"},
                    {"min_rate": "800000"}]
        }
        api.post(queueEndpoint, queueData)

    # Post Qos Rule
    ruleEndpoint = '/qos/rules/' + datapath
    #ruleData = {"match": {"ip_dscp": "26"},
    #            "actions": {"queue": "1"}}
    
    ruleData1 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5001"}, "actions":{"queue": "0"}}
    ruleData2 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions":{"queue": "1"}}
    ruleData3 = {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5003"}, "actions":{"queue": "2"}}
    
    api.post(ruleEndpoint, ruleData1)
    api.post(ruleEndpoint, ruleData2)
    api.post(ruleEndpoint, ruleData3)

    # Post Mark Rule
    #markEndpoint = '/qos/rules/' + datapath
    # markData = {"match": {"nw_dst": "10.0.0.1",
    #                  "nw_proto": "UDP",
    #                  "tp_dst": "5002"},
    #            "actions": {"mark": "26"}}
    #api.post(markEndpoint, markData)


def TreeNet( depth=1, fanout=2, **kwargs ):
    "Convenience function for creating tree networks."
    topo = TreeTopo( depth, fanout )
    return Mininet( topo, controller=RemoteController,**kwargs )

def connectToRootNS( network, switch, ip, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    intf = network.addLink( root, switch ).intf1
    root.setIP( ip, intf=intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

def Run( network, cmd='/usr/sbin/sshd', opts='-D',
          ip='10.123.123.1/32', routes=None, switch=None ):
    """Start a network, connect it to root ns, and run sshd on all hosts.
       ip: root-eth0 IP address in root namespace (10.123.123.1/32)
       routes: Mininet host networks to route to (10.0/24)
       switch: Mininet switch to connect to root namespace (s1)"""
    if not switch:
        switch = network[ 's1' ]  # switch to use
    if not routes:
        routes = [ '10.0.0.0/24' ]
    connectToRootNS( network, switch, ip, routes )
    for host in network.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    info( "*** Waiting for ssh daemons to start\n" )
    for server in network.hosts:
        waitListening( server=server, port=22, timeout=5 )

    info( "\n*** Hosts are running sshd at the following addresses:\n" )
    for host in network.hosts:
        info( host.name, host.IP(), '\n' )
 
    ####################
    ####################
    ####################
    # Get nodes
    s1 = net.get( 's1' )
    h1 = net.get('h1')
    h2 = net.get('h2')

    # Iniciar controlador
    info('*** Iniciando ryu...')
    try:
        info('por ahora no ejecutamos ryu aca...')
        #os.system('ryu-manager  ryu.app.qos_simple_switch_13_CAC ryu.app.qos_simple_switch_rest_13_CAC ryu.app.rest_conf_switch ryu.app.rest_qos &')
    except ValueError:
        info('Error...')

    sleep(2)

    # Configurar protocolo y manager
    info('*** Configurando OpenFlow13 en s1')
    s1.cmd( 'ovs-vsctl set Bridge s1 protocols=OpenFlow13' )
    info('*** Configurando OVSDB port') 
    s1.cmd( 'ovs-vsctl set-manager ptcp:6632' )

    # Configurar QoS
    info( '*** Configurando QoS...' )
    try:
        qosSetup(1) 
        sleep(2)
    except ValueError:
        print('Error....')
    
    #wireshark
    h1.cmdPrint('wireshark &')
    sleep(5)
    
    # Ejecutamos pruebas
    iperfTest(h1, h2)
    qosSetup(2)
    iperfTest(h1, h2)
    qosSetup(1)
    iperfTest(h1, h2)
    #aca continuar con pruebas con mas escenarios
    ####################
    ####################
    ####################

    info( "\n*** Type 'exit' or control-D to shut down network\n" )
    CLI( network )
    for host in network.hosts:
        host.cmd( 'kill %' + cmd )
    network.stop()

    # Destruir qos y colas
    info('*** Delete qos and queues in s1...')
    s1.cmdPrint('ovs-vsctl --all destroy QoS')
    s1.cmdPrint('ovs-vsctl --all destroy queue')
    sleep(2)

if __name__ == '__main__':
    lg.setLogLevel( 'info')
    net = TreeNet( depth=1, fanout=4 )
    # get sshd args from the command line or use default args
    # useDNS=no -u0 to avoid reverse DNS lookup timeout
    argvopts = ' '.join( sys.argv[ 1: ] ) if len( sys.argv ) > 1 else (
        '-D -o UseDNS=no -u0' )
    Run( net, opts=argvopts )
