## Leer API DOC MININET
- https://github.com/mininet/mininet/wiki/Introduction-to-Mininet#apilevels
- https://inside-openflow.com/2016/06/29/custom-mininet-topologies-and-introducing-atom/

### Ejecutar Minimal.py Custom Topology
    ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest
    sudo mn --custom minimal.py --topo minimal --controller remote

o bien:

    sudo python minimal.py

### Ejecutar DatacenterBasic.py Topology
    sudo mn --custom datacenterBasic.py --topo dcbasic --mac --switch ovs --controller remote

### Ejecutar DatacenterConfigurable.py
    sudo mn --custom datacenterConfigurable.py --topo dcconfig,2,8 --mac --switch ovs --controller remote