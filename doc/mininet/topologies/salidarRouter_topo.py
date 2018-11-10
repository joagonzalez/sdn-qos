from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, Controller, RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from os import system 

'''
           r0 10.0.0.254
           |  iprouter
           |  gwrouter
           |
h1 ------- s1 ------ h2
10.0.0.1             10.0.0.2
'''

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class MyTopo( Topo ):
    "Test topology"

    def build( self, **opts ):

        defaultIP = '10.0.0.254/8'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )

        # add switch
        s1 = self.addSwitch( 's1' )

        self.addLink( s1, router, intfName2='r0-eth1', params2={ 'ip': defaultIP } )

        # add hosts
        h1 = self.addHost( 'h1', defaultRoute='10.0.0.254' )
        h2 = self.addHost( 'h2', defaultRoute='10.0.0.254' )
        
        self.addLink( h1, s1 )
        self.addLink( h2, s1 )


def run():
    topo = MyTopo()
    net = Mininet( topo=topo, controller=RemoteController, autoSetMacs=True )
    net.start()

    # Get nodes
    router = net.get( 'r0' )
    controller = net.get( 'c0' )
    s1 = net.get( 's1' )
    h1 = net.get( 'h1' )
    h2 = net.get( 'h2' )
    
    iprouter = '10.0.3.56/24'
    gwrouter = '10.0.3.15'

    # Configurar nodos
    router.cmd( 'ip address add ' + iprouter + ' dev r0-eth1' )
    router.cmd( 'ip route add default via ' + gwrouter ) 
    h1.cmd( 'ip route add default via 10.0.0.254' ) 
    h2.cmd( 'ip route add default via 10.0.0.254' ) 

    # Setear nat en r0
    info( '*** Configurando NAT\n' )
    router.cmd( 'iptables -t nat -A POSTROUTING -o r0-eth1 -j MASQUERADE' )
    router.cmd( 'iptables -A FORWARD -i r0-eth1 -o r0-eth1 -m state --state RELATED ESTABLISHED -j ACCEPT' )
    router.cmd( 'iptables -A FORWARD -i eth1 -o r0-eth1 -j ACCEPT' )

    # Iniciar Controlador
    info( '*** Iniciando controlador\n' )
    controller.cmd( 'ryu-manager ryu.app.simple_switch_13 &' )

    # Agregar puerto fisico ethernet a s1
    system( 'ovs-vsctl add-port s1 enp0s3' )


    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
