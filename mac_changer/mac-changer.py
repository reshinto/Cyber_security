#!/usr/bin/env python3

import subprocess  # required to run shell commands
import optparse  # required for getting user input from args


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--shell", dest="shell",
            help="shell command for ip address (eg. ifconfig)")
    # give -i or --interface option, store in dest, give help if user requires
    parser.add_option("-i", "--interface", dest="interface",
            help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac",
            help="New MAC address")
    return parser.parse_args()  # return options & arguments  value


def change_mac(shell, interface, new_mac):
    # disable ethernet_interface if it exist
    subprocess.call([shell, interface, "down"])
    # change ethernet_interface's mac address
    subprocess.call([shell, interface, "hw", "ether", new_mac])
    # enable ethernet_interface
    subprocess.call([shell, interface, "up"])
    print(f"MAC address has been changed to {new_mac} for {interface}")


(options, arguments) = get_arguments()
change_mac(options.shell, options.interface, options.new_mac)
