'''
Simulacion QoS Mininet
'''

from  time import sleep
from loggerService import loggerService

from MyTopo import MyTopo
from Simulation import Simulation

from mininet.node import Node, Controller, RemoteController
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf

CONTROLLER_IP = '0.0.0.0'
CONTROLLER_API_PORT = '8080'
CONTROLLER_PORT = 6633
SIMULATION_TIME = 20

def run():
    topo = MyTopo()
    simulation = Simulation(CONTROLLER_IP, CONTROLLER_API_PORT)   
    controller = RemoteController( 'c0', ip='127.0.0.1', port=CONTROLLER_PORT )
    net = Mininet( topo=topo, controller=controller, autoSetMacs=True )
    
    net.start()

    # Obtenemos nodos de la topologia
    [s1, s2] = [net.get('s1'), net.get('s2')]
    [h1, h2] = [net.get('h1'), net.get('h2')]
    switches = [s1, s2]    
    hosts = [h1, h2]
    ports = ['5001', '5002', '5003']
    sleep(3)

    # Configuramos OVSDB Server
    simulation.conf_ovsdb_ovs(switches)
    sleep(2)

    # Inicializamos wireshark
    h1.cmdPrint('wireshark &')
    sleep(5)

    # Comenzamos simulacion
    loggerService.info( '*** Configuramos DSCP tags...' )
    simulation.dscp_mark(2)   
    loggerService.info( '*** Configuramos QOS queues...' )
    simulation.qosSetup(1, 1) 
    simulation.iperfTest(hosts, ports, SIMULATION_TIME)
    
    loggerService.info( '*** Configurando DSCP tags...' )
    simulation.dscp_mark(2)
    loggerService.info( '*** Configuramos QOS queues...' )
    simulation.qosSetup(2, 1)
    simulation.iperfTest(hosts, ports, SIMULATION_TIME)
    
    loggerService.info( '*** Configurando DSCP tags...' )
    simulation.dscp_mark(2)
    loggerService.info( '*** Configuramos QOS queues...' )
    simulation.qosSetup(1, 1)
    simulation.iperfTest(hosts, ports, SIMULATION_TIME)

    # Inicializamos Mininet CLI 
    CLI( net )
    net.stop()

    # Borramos QoS rules y queues
    simulation.deleteQoS(switches)
    sleep(2)    
   
if __name__ == '__main__':
    run()