#!/usr/bin/env python3


import scapy.all as scapy


def scan(ip):
    """
    Scans the ip address input to find the MAC address of the respective
    ip address by using the Address Resolution Protocol (arp) method:
    scapy.arping(xxx)
    """
    # writing our own arp method to discover clients on network
    # Create arp request directed to broadcast MAC asking for IP
    # has 2 main parts
    # Part 1: Use ARP to ask who has target IP
    """
    scapy.ARP() class allows us to print a summary of the current objects
    that we just created
    """
    arp_request = scapy.ARP(pdst=ip)

    # Part 2: Set destination MAC to broadcast MAC
    # create an ethernet object
    # use dst: DestMACField as arg, search by scapy.ls(scapy.Ether())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # combine request and broadcast with /
    arp_request_broadcast = broadcast/arp_request
    print(arp_request_broadcast.summary())


# 1/24 = range from 0 to 254
# this will allow you to scan all ip address
# real ip, use e.g.: xxx.xxx.1.1/24
scan("10.0.2.1/24")
