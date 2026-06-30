#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

SWITCH_COUNT = 196
HOST_COUNT = 91
CONTROLLER_IP = "floodlight"
CONTROLLER_PORT = 6653

def dpid_for_switch(index: int) -> str:
    return f"{index:016x}"

def build_topology():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True, autoStaticArp=False)
    info("*** Adding Floodlight remote controller\n")
    net.addController("c0", controller=RemoteController, ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    info(f"*** Creating {SWITCH_COUNT} switches\n")
    switches = [net.addSwitch(f"s{i}", dpid=dpid_for_switch(i), protocols="OpenFlow13") for i in range(1, SWITCH_COUNT + 1)]
    info("*** Creating switch chain\n")
    for i in range(SWITCH_COUNT - 1):
        net.addLink(switches[i], switches[i + 1], port1=2, port2=1)
    info(f"*** Creating {HOST_COUNT} hosts\n")
    hosts = [net.addHost(f"h{i}", ip=f"10.0.0.{i}/24", mac=f"00:00:00:00:00:{i:02x}") for i in range(1, HOST_COUNT + 1)]
    info("*** Attaching hosts\n")
    net.addLink(hosts[0], switches[0], port2=3)
    net.addLink(hosts[-1], switches[-1], port2=3)
    used_host_ports = {1: 3, SWITCH_COUNT: 3}
    for h_index in range(2, HOST_COUNT):
        sw_index = int((h_index - 1) * (SWITCH_COUNT - 1) / (HOST_COUNT - 1)) + 1
        sw_index = max(1, min(SWITCH_COUNT, sw_index))
        port = used_host_ports.get(sw_index, 3) + 1
        used_host_ports[sw_index] = port
        net.addLink(hosts[h_index - 1], switches[sw_index - 1], port2=port)
    info("*** Starting network\n")
    net.start()
    info("*** Adding static ARP entries between h1 and h91\n")
    hosts[0].setARP("10.0.0.91", "00:00:00:00:00:5b")
    hosts[-1].setARP("10.0.0.1", "00:00:00:00:00:01")
    info("*** Network is ready. After installing rules, test with: h1 ping -c 3 h91\n")
    CLI(net)
    info("*** Stopping network\n")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    build_topology()
