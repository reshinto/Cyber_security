#!/usr/bin/env python3

import subprocess  # required to run shell commands
import optparse  # required for getting user input from args
import re


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
        p.error("[-] Please specify a shell command, use --help for more info")
    elif not _options.interface:
        p.error("[-] Please specify an interface, use --help for more info")
    elif not _options.new_mac:
        p.error ("[-] Please specify a new MAC address, use --help for more info")
    return _options


def change_mac(shell, interface, new_mac, old_mac="hidden"):
    """
    Disable interface -> change MAC address -> enable interface
    """
    print(f"Changing MAC address from {old_mac} to {new_mac} for {interface}")
    subprocess.call([shell, interface, "down"])
    subprocess.call([shell, interface, "hw", "ether", new_mac])
    subprocess.call([shell, interface, "up"])


def get_MAC(shell, interface):
    # requires .decode("utf-8") if using python3
    output = subprocess.check_output([shell,
        interface]).decode("utf-8")
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
            output)
    if search_result:
        # use xxx.group(0) to display 1st search result
        return search_result.group(0)
    else:
        return "[-] Could not find MAC address"


def check_change(old="hidden"):
    _current = get_MAC(options.shell, options.interface)
    if _current == options.new_mac:
        print(f"[+] MAC address was successfully changed from {old} to {_current}")
    else:
        print("[+] MAC address was not changed.")

options = get_arguments()
old_mac = get_MAC(options.shell, options.interface)
change_mac(options.shell, options.interface, options.new_mac, old_mac)

check_change(old_mac)

change_mac(options.shell, options.interface, old_mac)
print(f"current MAC address: {get_MAC(options.shell, options.interface)}")

