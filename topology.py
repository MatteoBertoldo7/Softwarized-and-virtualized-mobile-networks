#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.link import TCLink

class CustomTopology(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Aggiungi gli switch per le cinque slice
        wifi_switch = self.addSwitch('s1')
        iot_switch = self.addSwitch('s2')
        traffic_switch = self.addSwitch('s3')
        safety_switch = self.addSwitch('s4')
        communication_switch = self.addSwitch('s5')


        # Aggiungi gli host per le cinque slice (quinta non ha host)
        wifi_host1 = self.addHost('h11')
        wifi_host2 = self.addHost('h12')
        iot_host1 = self.addHost('h21')
        iot_host2 = self.addHost('h22')
        traffic_host1 = self.addHost('h31')
        traffic_host2 = self.addHost('h32')
        safety_host1 = self.addHost('h41')
        safety_host2 = self.addHost('h42')

        # Collegamenti tra switch delle slice
        self.addLink(wifi_switch, communication_switch, bw=500, delay='10ms', loss=0, use_htb=True)
        self.addLink(iot_switch, communication_switch, bw=20, delay='25ms', loss=0, use_htb=True)
        self.addLink(traffic_switch, communication_switch, bw=100, delay='2ms', loss=0, use_htb=True)
        self.addLink(safety_switch, communication_switch, bw=50, delay='8ms', loss=0, use_htb=True)

        # Collegamenti tra switch e host delle slice
        self.addLink(wifi_host1, wifi_switch)
        self.addLink(wifi_host2, wifi_switch)
        self.addLink(iot_host1, iot_switch)
        self.addLink(iot_host2, iot_switch)
        self.addLink(traffic_host1, traffic_switch)
        self.addLink(traffic_host2, traffic_switch)
        self.addLink(safety_host1, safety_switch)
        self.addLink(safety_host2, safety_switch)

        #creo i 5 server
        wifi_server = self.addHost('server1')
        iot_server = self.addHost('server2')
        traffic_server = self.addHost('server3')
        safety_server = self.addHost('server4')
        communication_server = self.addHost('server5')

        # collegamenti tra switch e server
        self.addLink(wifi_server, wifi_switch)
        self.addLink(iot_server, iot_switch)
        self.addLink(traffic_server, traffic_switch)
        self.addLink(safety_server, safety_switch)
        self.addLink(communication_server, communication_switch)



if __name__ == '__main__':
    topo = CustomTopology()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    net.build()

    # Configura il controller SDN (puoi personalizzare l'indirizzo IP e la porta)
    controller = RemoteController('c0', ip='127.0.0.1', port=6633)
    net.addController(controller)

    net.start()

    # Configura le regole di flusso o le limitazioni specifiche dei link
    # Puoi utilizzare il comando "net['switch'].cmd()" per aggiungere regole personalizzate

    # Esempio di impostazione di una limitazione di banda su una porta specifica del link tra s11 e s12
    net['s11'].cmd('tc qdisc add dev s11-eth1 root tbf rate 1Mbit burst 10kbit latency 10ms')

    CLI(net)
    net.stop()
