#!/usr/bin/python

"""
Example to create a Mininet topology and connect it to the internet via NAT
Modified to user a RemoteController
"""


from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topolib import TreeNet, TreeTopo
from mininet.node import RemoteController
from mininet.net import Mininet

if __name__ == '__main__':
    lg.setLogLevel( 'info')
    topo = TreeTopo( depth=1, fanout=4,  )
    
    net = Mininet( topo=topo, controller=RemoteController )
    
    # Add NAT connectivity
    net.addNAT().configDefault()
    net.start()
    info( "*** Hosts are running and should have internet connectivity\n" )
    info( "*** Type 'exit' or control-D to shut down network\n" )
    CLI( net )
    # Shut down NAT
    net.stop()
