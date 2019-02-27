#!/usr/bin/env python3
"""
Network scanner that scans for 1 or all IP addresses connected
within the same network, to get its MAC Address
Must run as admin: in mac or linux, use sudo
"""
import argparse
import scapy.all as scapy


def get_arguments():
    """
    Run and input IP address in the command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",
                        help="target IP address or range e.g.: 10.0.2.1/24")
    _args = parser.parse_args()
    if not _args.target:
        parser.error("[-] Please specify a target, use --help for more info")
    return _args


def scan(ip):
    """
    Scans the ip address input to find the MAC address
    """
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # use verbose to get rid of header text
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=1, verbose=False)[0]

    # parsing response
    clients_list = []
    for i in answered_list:
        client_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def show(clients_list):
    """prints list of IP and MAC addresses"""
    print("IP\t\tMAC Address\n" + "-"*40)
    for client in clients_list:
        print(f"{client['ip']}\t{client['mac']}")


def main():
    """Run main program"""
    arg = get_arguments()
    scan_result = scan(arg.target)
    show(scan_result)


if __name__ == "__main__":
    main()
