# CAC Application

## Initialize RYU Controller
$ ryu-manager son rest_qos qos_simple_switch_13 y rest_conf_switch

## Emulate Switches with mininet
$ sudo mn --topo single,5 --mac --switch ovsk --controller remote

## Modify OVS parameters OpenFlow13 and QoS support
ovs-vsctl set Bridge s1 protocols=OpenFlow13
ovs-vsctl set-manager ptcp:6632

## Modify simple_switch_13 in order to support multi tables in OpenFlow13

sed '/OFPFlowMod(/,/)/s/)/, table_id=1)/' ryu/ryu/app/simple_switch_13.py > ryu/ryu/app/qos_simple_switch_13.py
cd ryu/; python ./setup.py install

## Iniciar backend
# Dependencias con pip / te recomiendo instalar pyenv con python3.6
apt-get install pycurl
sudo pip install git+https://github.com/dpallot/simple-websocket-server
cac/backend$ python run.py

## Iniciar Mocks Ryu
cac/mocks$ npm install
cac/mocks$ npm start (localhost:8001)

## Iniciar Front End
# Instalar dependencias
cac/frontend$ npm install
cac/frontend$ npm start (localhost:3000)

## TODOS
- poner las configuraciones en un config.settings file (OK)
- armar logger file 
- poner baner
- Hacer unit test e integration tests corriendose en un makeFile
- Dockerizar la app en un container y las instancias del ari + ryu para soporte multiplataforma
- Buscar libreria de Grafos
- Armar frontend en React