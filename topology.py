#!/usr/bin/python3

#metto anche import os ?
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, RemoteController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import Controller

class CustomTopology(Topo):
    def __init__(self):
        #Initialize
        Topo.__init__(self)

        # Create host and switch configurations
        host_config = dict(inNamespace=True)
        switch_config = dict(protocols="OpenFlow13")

        # Create 5 switch nodes
        switches = []
        for i in range(5):
            switch = self.addSwitch("s%d" % (i + 1), **switch_config)
            switches.append(switch)

        # Create 10 host nodes
        for i in range(10):
            self.addHost("h%d" % (i + 1), **host_config)

        # Define QoS parameters for each slice
        qos_params = [
            {"slice_name": "Smart Traffic", "bw": 100, "delay": "10ms"},
            {"slice_name": "Public Safety", "bw": 50, "delay": "20ms"},
            {"slice_name": "IoT Monitoring", "bw": 200, "delay": "5ms"},
            {"slice_name": "Office", "bw": 20, "delay": "15ms"},
            {"slice_name": "Guest WiFi", "bw": 500, "delay": "2ms"},
        ]

        # Create links between hosts and switches with QoS parameters
        for i, host in enumerate(self.hosts):
            switch = switches[i % 5]
            qos = qos_params[i % 5]
            self.addLink(host, switch, **qos)

def main():
    topo = CustomTopology()
    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    main()
