#!/usr/bin/env python3

import subprocess  # required to run shell commands

ip_command = input("ip address shell command: ")
interface = input("ethernet interface (eg. eth0): ")
new_mac = input("new MAC (12 digits eg.00:11:22:33:44:55): ")

print(f"+ Changing MAC address for {interface} to {new_mac}")
# disable ethernet_interface if it exist
subprocess.call(f"{ip_command} {interface} down", shell=True)  # not safe
print(f"{interface} has been disabled")
# change ethernet_interface's mac address
subprocess.call(f"{ip_command} {interface} hw ether {new_mac}", shell=True)
print(f"mac address has been changed to {new_mac}")
# enable ethernet_interface
subprocess.call("{ip_command} {interface} up", shell=True)
print(f"{interface} has been enabled")

