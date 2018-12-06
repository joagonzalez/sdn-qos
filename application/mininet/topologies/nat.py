#!/usr/bin/python

"""
Example to create a Mininet topology and connect it to the internet via NAT
"""


from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topolib import TreeNet


if __name__ == '__main__':
    lg.setLogLevel( 'info')
    net = TreeNet( depth=1, fanout=4 )
    # Add NAT connectivity
    net.addNAT().configDefault()
    net.start()
    info( "*** Hosts are running and should have internet connectivity\n" )
    info( "*** Type 'exit' or control-D to shut down network\n" )
    CLI( net )
    # Shut down NAT
    net.stop()

#Crea NAT en el host para las redes 10.0.0.0/8
#CMD: sudo iptables -L | grep 10.0.0.0
#ACCEPT     all  --  10.0.0.0/8           anywhere            
#ACCEPT     all  --  anywhere             10.0.0.0/8
#CMD: sudo iptables -t nat -L -v | grep 10.0
#MASQUERADE  all  --  any  any  10.0.0.0/8 !10.0.0.0/8 
