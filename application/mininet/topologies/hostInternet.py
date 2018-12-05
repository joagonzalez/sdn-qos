#!/usr/bin/python

#### https://techandtrains.com/2013/11/24/mininet-host-talking-to-internet/

from mininet.net import Mininet
from mininet.node import Node, Controller, RemoteController
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info

def myNetwork():

    net = Mininet( topo=None, controller=RemoteController, 
                   build=False)

    info( '*** Adding controller\n' )
    #net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    Intf( 'eth2', node=s1 )

    info( '*** Add hosts\n')
    h1 = net.addHost('h1')
    #Si quiero que tome ip por DHCP
    #h1 = net.addHost('h1', ip='0.0.0.0')

    info( '*** Add links\n')
    net.addLink(h1, s1)

    info( '*** Starting network\n')
    net.start()
    #Si quiero que tome ip por DHCP
    #h1.cmdPrint('dhclient '+h1.defaultIntf().name)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()