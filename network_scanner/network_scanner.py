#!/usr/bin/env python3


import scapy.all as scapy


def scan(ip):
    """
    Scans the ip address input to find the MAC address
    """
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # use verbose to get rid of header text
    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return answered_list


def show(scanned_list_result):
    print("IP\t\t|\tMAC Address\n" + "-"*50)
    # parsing response
    for i in scanned_list_result:
        # psrc to display IP address, hwsrc to display MAC address
        print(f"{i[1].psrc}\t|\t{i[1].hwsrc}\n" + "-"*50)


# 1/24 = range from 0 to 254
# this will allow you to scan all ip address
# real ip, use e.g.: xxx.xxx.1.1/24
result = scan("10.0.2.1/24")
show(result)
