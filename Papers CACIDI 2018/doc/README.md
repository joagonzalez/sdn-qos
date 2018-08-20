# Paper Call Admission Control SDN

## Objetivo:

Implementar mecanismo de Call Admission Control (CAC) utilizando northbound APIs y OpenFlow sobre plataforma SIP. Tomar indicadores de BW, Jitter y Packet Loss como parámetros para medir performance y realizar comparaciones sobre una arquitectura no SDN. El desarrollo contemplara modelo de APIs, controlador y comunicación southbound interface con OpenFlow. (1.3, 1.5 y 1.6) 

- https://www.opennetworking.org/wp-content/uploads/2014/10/openflow-switch-v1.5.1.pdf

## Herramientas

- GNS3 (https://gns3.com/) - Virtualizador redes
- Mininet 2.2.2 Ubuntu 14 LTS (http://mininet.org/) - Network emulator con soporte de Open Flow basado en contenedores y OVS
- Open Virtual Switch (https://www.openvswitch.org/) - Software de switch virtual
- Onos (https://onosproject.org/) - Controlador SDN
- Faucet 1.8.9 (https://faucet.nz/) - Controlador SDN
- POSTman (https://www.getpostman.com/) - Desarrollo y monitoreo
- Mahimahi (http://mahimahi.mit.edu/) - Desarrollo y monitoreo
- Python/Java para desarrollo de API y aplicación en controlador
- Asterisk 13.14.1
- Debian 9.5 Stable
- Asterisk RESTful Interface (ARI) https://wiki.asterisk.org/wiki/pages/viewpage.action?pageId=29395573
- aripy modulo de Python para uso de ARI https://github.com/asterisk/ari-py 

## Casos de uso

Se tratan en detalle dos casos de uso por ser los más representativos en el uso de CAC y los mas implementados por proveedores de servicios. SDN jugaria un rol fundamental en este escenario para implementar CAC de forma dinámica bajo demanda de las aplicaciones SIP que utilizan la red. Por otro lado, con este mismo mecanismo podrían implementarse tags/configuraciones sobre colas QoS que permitan priorizar flujos en tiempo real, este es una posibilidad no existente en redes no SDN.

- MPLS: Se implementa Call Admission Control en un escenarios de conectividad MPLS. Multiples sitios distribuidos en distintas regiones conectados sobre una red MPLS en donde CAC debe ejecutar restricciones basandose en información de subredes origen/destino asociadas a cada sitio. Por otro lado, el vinculo que utilizará un sitio para comunicarse con el resto será compartido.

- WAN: Se implementa CAC en un escenario de conectividad punto a punto o enlaces WAN entre sitios. En este caso las distintas locaciones tendrán BW específico para conectarse a cada uno de los sitios por lo que las políticas deberan contemplar estas diferenencias.

## Bibliografía

Se puede encontrar y agregar/modificar en Papers de Referencia.


[1] Dynamic QoS on SIP Sessions Using OpenFlow

[2] Using Software-Defined Networking for Real Time Internet Applications

[3] https://github.com/yanlisa/reproducibility/wiki/Reproducing-Network-Research

[4] https://community.asterisk.org/t/ari-and-making-a-call-between-2-extensions-through-ari-client/66199/3 - Caso de control de canales entre dos extensiones tipo usuario