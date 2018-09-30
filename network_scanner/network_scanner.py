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

    # parsing response
    clients_list = []
    for i in answered_list:
        client_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def show(clients_list):
    print("IP\t\tMAC Address\n" + "-"*40)
    for client in clients_list:
        print(f"{client['ip']}\t{client['mac']}")


# 1/24 = range from 0 to 254
# this will allow you to scan all ip address
# real ip, use e.g.: xxx.xxx.1.1/24
scan_result = scan("10.0.2.1/24")
show(scan_result)
