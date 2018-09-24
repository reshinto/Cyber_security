#!/usr/bin/env python3

import subprocess  # required to run shell commands
import optparse  # required for getting user input from args


def change_mac(shell, interface, new_mac):
    print(f"+ Changing MAC address for {interface} to {new_mac}")
    # disable ethernet_interface if it exist
    # all commands run after index 0   is  a subcommand
    subprocess.call([shell, interface, "down"])
    print(f"{interface} has been disabled")
    # change ethernet_interface's mac address
    subprocess.call([shell, interface, "hw", "ether", new_mac])
    print(f"mac address has been changed to {new_mac}")
    # enable ethernet_interface
    subprocess.call([shell, interface, "up"])
    print(f"{interface} has been enabled")


parser = optparse.OptionParser()

parser.add_option("-s", "--shell", dest="shell",
        help="shell command for ip address (eg. ifconfig)")
# give -i or --interface option, store in dest, give help if user requires
parser.add_option("-i", "--interface", dest="interface",
        help="Interface to change MAC address")
parser.add_option("-m", "--mac", dest="new_mac",
        help="New MAC address")

# parser.parse_args() -> will allow user to parse but not return
# the following command
# eg.python mac-changer.py -s ifconfig -i eth0 -m 00:11:22:33:44:55
(options, arguments) = parser.parse_args()  # return options & arguments  value

change_mac(options.shell, options.interface, options.new_mac)
