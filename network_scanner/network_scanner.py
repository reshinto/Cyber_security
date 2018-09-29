#!/usr/bin/env python3


import scapy.all as scapy


def scan(ip):
    """
    Scans the ip address input to find the MAC address of the respective
    ip address by using the Address Resolution Protocol (arp) method:
    scapy.arping(xxx)
    """
    scapy.arping(ip)


# 1/24 = range from 0 to 254
# this will allow you to scan all ip address
# real ip, use e.g.: xxx.xxx.1.1/24
scan("10.0.2.1/24")
