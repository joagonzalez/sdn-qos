# CAC Application

## Initialize RYU Controller
$ ryu.app.simple_switch_13 ryu.app.simple_switch_rest_13 ryu.app.rest_conf_switch

### Initialize Ryu Controller QoS test
$ ryu-manager ryu.app.qos_simple_switch_13_CAC ryu.app.qos_simple_switch_rest_13_CAC ryu.app.rest_conf_switch ryu.app.rest_qos

### Initialize Ryu Controller test
$ ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest

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
- Armar un jenkins y automatizar todo el deploy en 1 solo script
- Poner base de datos para grabar cosas interesantes (un postgres o un mongodb livianito.. o un sqlite porque no)
- Falta investigar mininet

## CAC - Docker - Infraestructura Automatizada
- 1 Dockerfile por servicio
- 1 docker-compose.yml para orquestar los servicios en modo Swarm con una network default en bridge mode.
- Comandos:
  - docker-compose -f docker-compose.yml up (corre todas las instancias. Si no existen las imagenes, las buildea)
  - docker-compose down
  - docker stack deploy (deploya los servicios en un stack consumible por docker service)
  - docker container ls (muestra los running containers)
  - docker image ls (muestra las imagenes actuales)
  - docker network ls (muestra las interfaces creadas por docker)
  - docker build -t imageName /abs/path/to/dockerfile (buildea una imagen desde un Dockerfile)

- Cosas interesantes
  - wait-for-it.sh = es un script que se utiliza dentro de los containers para escuchar que exista un proceso dentro de la red de los containers. cac-backend utiliza esto ya que necesita esperar que el ryu y el asterisk esten realmente ya en linea, permitiendo asi, el orden en tiempo y forma del flujo de los procesos como deben ser iniciados por sus respectivas dependencias.

