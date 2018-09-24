#!/usr/bin/env python3

import subprocess  # required to run shell commands
import optparse  # required for getting user input from args


def get_arguments():
    """
    Run and input the following:
    python mac-changer.py -s ifconfig -i eth0 -m 00:11:22:33:44:55
    then return the argument values
    """
    p = optparse.OptionParser()
    p.add_option("-s", "--shell", dest="shell",
            help="shell command for ip address (eg. ifconfig)")
    p.add_option("-i", "--interface", dest="interface",
            help="Interface to change MAC address")
    p.add_option("-m", "--mac", dest="new_mac",
            help="New MAC address")
    (_options, _arguments) = p.parse_args()
    if not _options.shell:
        # code to handle error
        p.error("[-] Please specify a shell command, use --help for more info")
    elif not _options.interface:
        p.error("[-] Please specify an interface, use --help for more info")
    elif not _options.new_mac:
        # code to handle error
        p.error ("[-] Please specify a new MAC address, use --help for more info")
    return _options


def change_mac(shell, interface, new_mac):
    """
    Disable interface -> change MAC address -> enable interface
    """
    subprocess.call([shell, interface, "down"])
    subprocess.call([shell, interface, "hw", "ether", new_mac])
    subprocess.call([shell, interface, "up"])
    print(f"MAC address has been changed to {new_mac} for {interface}")


options = get_arguments()
change_mac(options.shell, options.interface, options.new_mac)
