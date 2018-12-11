#!/usr/bin/python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI, info

setLogLevel( 'info' )

# Two local and one "external" controller (which is actually c0)
# Ignore the warning message that the remote isn't (yet) running
#c0 = Controller( 'c0', port=6633 )
#c1 = Controller( 'c1', port=6634 )
#127 es ryu en localhost
c1 = RemoteController( 'c1', ip='127.0.0.1', port=6633 )

net = Containernet(controller=c1)

info('*** Adding switches\n')
s1 = net.addSwitch('s1')

topo = TreeTopo( depth=1, fanout=1 )
net = Mininet( topo=topo, build=False )

net.addController(c1)
net.build()
net.start()
CLI( net )
net.stop()
