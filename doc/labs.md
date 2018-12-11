### Lab 1 (vm)

ryu-manager ryu.app.simple_switch_13 ryu.app.simple_switch_rest_13 ryu.app.rest_conf_switch
sudo python run.py
npm start
sudo mn --controller remote
sipp -d 10000 -s 1000 192.168.56.101 -l 5 -mp 5606 -i 192.168.56.1
sipp -d 10000 -s 7000 192.168.56.101 -l 5 -mp 5606 -i 192.168.56.1
ssh 192.168.56.101 -> sudo asterisk -r
sudo tshark -i any -Y "rtp or sip"
sudo tshark -i wlp1s0 -e ip.src -e ip.dst -e frame.time -T fields


### Lab 2 (containers + socket/parser)

sudo docker-compose -f docker-compose.yml up
docker  build -t ryu-controller .
docker  build -t asterisk-ari .
docker  build -t cac-frontend .
docker  build -t cac-backend .
docker  build -t cac-mininet .
docker  build -t cac-simulation-caller .

### Sipp python library
https://github.com/pbertera/SIPp-by-example
https://github.com/SIPp/pysipp

### Goals tuesday 11th

1) Finish tcpdump/tshark parsing
2) Solve back end app within container (run(cac)) -- OK
3) Grafico frontend trafficReporter
4) CAC simulations in containter scenario -- OK
5) Modify Stasis App to achieve better performance with rtp overhead
6) (optional) apply QoS within simulation scenarios

#### CAC performance

- CAC apunta a la experiencia del usuario. El usuario no tendra ni 1 segundo de audio cuando la llamada sea finalizada, por lo que el objetivo de que no ocurra sera exitoso en terminos de QoE

- El trafico excendente ocupara la cola al final, por lo que el poco tiempo de RTP que exceda la queue sera descartado y no sera relevante

- El usuario medido es el peor de todos, pues un robot atiende inmediatamente y las llamadas son disparadas por un simulador, lo que genera RTP de manera constante

- Un approach para solucionar esto e implementar CAC de una manera diferente consiste en no disparar la llamada con el originate siquiera cuando el umbral se excede. De esta manera no habra overhead de RTP en la red cuando actue CAC

- Tambien podria implementarse un mecanismo de queueing para tratar las llamadas excedentes

#### Documentacion simulaciones por branch

- Nombre simulacion: CAC Calls Containers sipp
- Repositorio: sdn-qos
- Branch: cac-be-with-gui-topology-call-simulation-and-graphic-traffic-ovs-over-mn
- Video loom: CAC App v2 with sipp simulation and topology ryu module
- Descripcion: Levantar docker-compose -f docker-compose.yml up

- Nombre simulacion: QoS Real-Time with mininet and Ryu (DSCP+queues)
- Repositorio: SDN-Call-Admission-Control
- Branch: CAC_App_v1_refactor
- Video loom: QoS Real-Time with mininet and Ryu (DSCP+queues)
- Descripcion: Se ejecutan asterisk (vm), backend, frontend, ryu y mininet con la topologia establecida y luego la simulacion script sdn-qos-RealTimeQueues.py en folder mininet/ del repo

- Nombre simulacion: CAC vs no-CAC scenario and sipp (new hangup method)
- Repositorio: SDN-Call-Admission-Control
- Branch: CAC_App_v1_refactor
- Video loom: CAC vs no-CAC scenario and sipp
- Descripcion: Se ejecutaran llamadas a una extension no expuesta por aplicacion Stasis (1000) y a otra expuesta por aplicacion Stasis(cac) (7000) y se compararan resultados para entender comportamiento de aplicacion CAC

