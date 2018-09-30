#!/usr/bin/env python3


import scapy.all as scapy


def scan(ip):
    """
    Scans the ip address input to find the MAC address of the respective
    ip address by using the Address Resolution Protocol (arp) method:
    scapy.arping(xxx)
    """
    # writing our own arp method to discover clients on network
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # send packet & receive response
    """send & receive function
    there is also a scapy.sr()
    difference between srp and sr is, srp allows us to send packets with
    a custom Ether packet
    add timeout you quit if get no response within 1 sec
    """
    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1)
    print(answered.summary())


# 1/24 = range from 0 to 254
# this will allow you to scan all ip address
# real ip, use e.g.: xxx.xxx.1.1/24
scan("10.0.2.1/24")
