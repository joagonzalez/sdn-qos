import os
import json
from  time import sleep

from loggerService import loggerService
from api import ApiService

class Simulation:
    SIMULATION_TIME = 5
    QOS_RULES = '/qos/rules/'
    QOS_QUEUES = '/qos/queues/'
    OVSDB_CONF = '/v1.0/conf/switches/'
    OVSDB_SERVER = "tcp:127.0.0.1:6632"

    def __init__(self, controllerIp, controllerPort):
        self.controllerUrl = self.controller_query(controllerIp, controllerPort)
        self.api = ApiService(self.controllerUrl)
        
    def switch_query(self, switch):
        '''
        switch datapath creator
        '''
        datapath = '000000000000000' + str(switch)
        return datapath

    def controller_query(self, ip, port):
        controllerUrl = 'http://' + ip + ':' + port
        return controllerUrl

    def conf_ovsdb_ovs(self, switches):
        i = 1
        for switch in switches:
            s = 's' + str(i)
            loggerService.info('*** Configurando OpenFlow13 en ' + s)
            switch.cmd( 'ovs-vsctl set Bridge ' + s + ' protocols=OpenFlow13' )
            loggerService.info('*** Configurando OVSDB port') 
            switch.cmd( 'ovs-vsctl set-manager ptcp:6632' )
            i = i + 1

    def deleteQoS(self, switches):
        loggerService.info('*** Borrando QoS rules y queues...')
        for switch in switches:
            switch.cmdPrint('ovs-vsctl --all destroy QoS')
            switch.cmdPrint('ovs-vsctl --all destroy queue')

    # Tagging de campo Type of Service con DSCP
    def dscp_mark(self, switch):
        datapath = self.switch_query(switch)
        api = self.api

        # Reglas DSCP
        endpoint = self.QOS_RULES + datapath
        rules = [{"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5001"}, "actions": {"mark": "26"}},
                 {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5002"}, "actions": {"mark": "10"}},
                 {"match": {"nw_dst": "10.0.0.1", "nw_proto": "UDP", "tp_dst": "5003"}, "actions": {"mark": "12"}}
        ]

        # Queries API
        for rule in rules:
            api.post(endpoint, rule)

    # iperfTest simulate best effort traffic between hosts
    def iperfTest(self, hosts, testPorts, time):
        loggerService.debug("Inicializar simulacion de trafico con IPerf")
        server = hosts[0]
        client = hosts[1]

        for port in testPorts:
        #iperf Server
            server.cmdPrint('iperf -s -u -p ' + str(port) + ' -i 1 > results' + str(port) + ' &')

        for port in testPorts:
        #iperf Client
            client.cmdPrint('iperf -c ' + server.IP() + ' -u -t ' + str(time) + ' -i 1 -p ' + str(port) + ' -b 1M &')
        
        sleep(self.SIMULATION_TIME)
        client.cmdPrint('killall -9 iperf')
        server.cmdPrint('killall -9 iperf')

    def pingAll(self, net):
        loggerService.debug("Comenzamos pingall ")
        net.pingAll()

    def qosSetup(self, test, switch):
        '''
        Configurar qos queues en switches
        '''

        datapath = self.switch_query(switch)
        endpoint = self.OVSDB_CONF + datapath + '/ovsdb_addr'
        self.api.put(endpoint, self.OVSDB_SERVER)
        sleep(2)

        # Post Queue
        if test == 1:
            queueEndpoint = '/qos/queue/' + datapath
            queueData = {
                "port_name": "s" + str(switch) + "-eth1",
                "type": "linux-htb",
                "max_rate": "1000000",
                "queues": [{"max_rate": "100000"},
                        {"max_rate": "200000"},
                        {"max_rate": "300000"},
                        {"min_rate": "800000"}]
            }

            self.api.post(queueEndpoint, queueData)
        else:
            queueEndpoint = '/qos/queue/' + datapath
            queueData = {
                "port_name": "s" + str(switch) + "-eth1",
                "type": "linux-htb",
                "max_rate": "1000000",
                "queues": [{"max_rate": "200000"},
                        {"max_rate": "300000"},
                        {"max_rate": "100000"},
                        {"min_rate": "800000"}]
            }
            self.api.post(queueEndpoint, queueData)

        endpoint = self.QOS_RULES + datapath
        
        rules = [{"match": {"ip_dscp": "26"}, "actions":{"queue": "0"}},
                 {"match": {"ip_dscp": "10"}, "actions":{"queue": "1"}},
                 {"match": {"ip_dscp": "12"}, "actions":{"queue": "2"}}
        ]
        
        for rule in rules:
            try:
                self.api.post(endpoint, rule)
            except Exception as e:
                loggerService.error('Error configurando reglas qos en controlador')
