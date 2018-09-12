# CAC Application

## Initialize RYU Controller
$ ryu-manager son rest_qos qos_simple_switch_13 y rest_conf_switch

## Emulate Switches with mininet
$ sudo mn --topo single,5 --mac --switch ovsk --controller remote

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
- poner las configuraciones en un config.settings file
- Hacer unit test e integration tests
- Dockerizar la app en un container y las instancias del ari + ryu para soporte multiplataforma
- Buscar libreria de Grafos
- Armar frontend en React