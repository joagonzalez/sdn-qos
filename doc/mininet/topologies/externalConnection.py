#!/usr/bin/python

"""
A simple minimal topology script for Mininet.

Based in part on examples in the [Introduction to Mininet] page on the Mininet's
project wiki.

[Introduction to Mininet]: https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#apilevels

"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.node import Node, Controller, RemoteController

class MinimalTopo( Topo ):
    "Minimal topology with a single switch and three hosts"

    def build( self ):
        # Create two hosts.
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )

        # Create a switch
        s1 = self.addSwitch( 's1' )

        # Add links between the switch and each host
        self.addLink( s1, h1 )
        self.addLink( s1, h2 )
        self.addLink( s1, h3 )

def runMinimalTopo():
    "Bootstrap a Mininet network using the Minimal Topology"

    # Create an instance of our topology
    topo = MinimalTopo()

    # Create a network based on the topology using OVS and controlled by
    # a remote controller.
    net = Mininet(
        topo=topo,
        controller=RemoteController,
        switch=OVSSwitch,
        autoSetMacs=True )

    # Actually start the network
    net.start()

    # Get nodes
    # hosth1 = net.get('h1')
    # hosth2 = net.get('h2')
    s1 = net.get('s1')
    controller = net.get( 'c0' )
    h1 = net.get( 'h1' )
    h2 = net.get( 'h2' )

    # Iniciar Controlador
    #info( '*** Iniciando controlador\n' )
    #controller.cmd( 'ryu-manager ryu.app.qos_simple_switch_13_CAC ryu.app.qos_simple_switch_rest_13_CAC ryu.app.rest_conf_switch ryu.app.rest_qos &' )

    s1.cmdPrint('ovs-vsctl set-manager ptcp:6632')
    s1.cmdPrint('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    s1.cmdPrint('ovs-vsctl show')
    s1.cmdPrint('ovs-ofctl -O OpenFlow13 show s1')
    net.pingAll()
    # hosth1.cmdPrint('ping ' + hosth2.IP())

    # Agregar puerto fisico ethernet a s1
    info( '*** Agregando interfaz fisica al Switch s1\n' )
    s1.cmdPrint('ovs-vsctl add-port s1 enp0s8' )

    #Config h1 IP()
    h1.cmdPrint('ifconfig h1-eth0 0')
    h1.cmdPrint('ifconfig h1-eth0 10.0.3.46/24')

    # Drop the user in to a CLI so user can run commands.
    CLI( net )

    # After the user exits the CLI, shutdown the network.
    net.stop()

if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    runMinimalTopo()

# Allows the file to be imported using `mn --custom <filename> --topo minimal`
topos = {
    'minimal': MinimalTopo
}