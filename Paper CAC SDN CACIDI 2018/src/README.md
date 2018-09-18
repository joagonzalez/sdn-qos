# CAC Application

## Initialize RYU Controller
$ ryu-manager ryu.app.simple_switch_13 ryu.app.simple_switch_rest_13 ryu.app.rest_conf_switch

### Initialize Ryu Controller QoS test
$ ryu-manager ryu.app.qos_simple_switch_13_CAC ryu.app.simple_switch_rest_13_CAC ryu.app.rest_conf_switch ryu.app.rest_qos

### Initialize Ryu Controller test
$ ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest

## Emulate Switches with mininet
$ sudo mn --topo single,5 --mac --switch ovsk --controller remote
(falta comandos para configurar en kernel space)

## Iniciar Backend
cac/backend$ python run.py

### Dependencias con pip y apt-get
apt-get install pycurl
sudo pip install git+https://github.com/dpallot/simple-websocket-server

## Iniciar Mocks Ryu (deprecado, ir directo contra Ryu)
cac/mocks$ npm install
cac/mocks$ npm start (localhost:8001)

## Iniciar Front End
cac/frontend$ npm start (localhost:3000)

### Instalar dependencias
cac/frontend$ npm install

## TODOS

### Fase 1
- Terminar de programar metodos de clases para interaccion basica de la plataforma (app stasis Ari y queries Ryu)
- poner las configuraciones en un config.settings file
- Armar grafico con ws y API connections con puertos para cada modulo
- Diagrama de clases con metodos 

### Fase 2
- Dockerizar la app en un container y las instancias del ari + ryu para soporte multiplataforma
- Buscar libreria de Grafos
- Armar frontend en React -> Reemplazar a futuro con Flask (Pablo B. idea)