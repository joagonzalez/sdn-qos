# modulos mininet
from mininet.topo import Topo

class MyTopo( Topo ):
    '''
    Clase para definir topologia a desplegar con Mininet
    '''


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
