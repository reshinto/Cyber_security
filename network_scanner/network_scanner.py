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
    # use verbose to get rid of header text
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    print("IP\t\t|\tMAC Address\n" + "-"*50)
    # parsing response
    for i in answered_list:
        # psrc to display IP address, hwsrc to display MAC address
        print(f"{i[1].psrc}\t|\t{i[1].hwsrc}\n" + "-"*50)


# 1/24 = range from 0 to 254
# this will allow you to scan all ip address
# real ip, use e.g.: xxx.xxx.1.1/24
scan("10.0.2.1/24")
