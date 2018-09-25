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
        p.error(
            "[-] Please specify a shell command, use --help for more info")
    elif not _options.interface:
        p.error("[-] Please specify an interface, use --help for more info")
    elif not _options.new_mac:
        p.error(
            "[-] Please specify a new MAC address, use --help for more info")
    return _options


def change_mac(shell, interface, new_mac, hw=None):
    """
    shell = ifconfig
    Disable interface -> change MAC address -> enable interface
    """
    print(f"[+] Changing MAC address for {interface}")
    subprocess.call([shell, interface, "down"])
    _change_mac(shell, interface, new_mac, hw)
    subprocess.call([shell, interface, "up"])


def _change_mac(shell, interface, new_mac, hw=None):
    """
    Check if hw is required
    hw is required for Kali linux
    """
    if hw is None:
        subprocess.call([shell, interface, "ether", new_mac])
    else:
        subprocess.call([shell, interface, hw, "ether", new_mac])


def new_change_mac(shell, interface, new_mac):
    """
    shell = ip
    """
    print(f"[+] Changing MAC address for {interface}")
    subprocess.call([shell, "link", "set", "dev", interface, "down"])
    subprocess.call(
        [shell, "link", "set", "dev", interface, "address", new_mac])
    subprocess.call([shell, "link", "set", "dev", interface, "up"])


def get_mac(shell, interface):
    """Extract MAC address output"""
    # requires .decode("utf-8") if using python3
    output = _get_mac(shell, interface)
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                              output)
    if search_result:
        # use xxx.group(0) to display 1st search result
        return search_result.group(0)
    return "[-] Could not find MAC address"


def _get_mac(shell, interface):
    """Search for MAC address"""
    if shell == "ifconfig":
        return subprocess.check_output(
            [shell, interface]).decode("utf-8")
    elif shell == "ip":
        return subprocess.check_output(
            [shell, "addr", "show", interface]).decode("utf-8")
    return "TODO"  # "ipconfig"


def check_change(shell, interface, new_mac):
    """Check if MAC address has been changed"""
    _current = get_mac(shell, interface)
    if _current == new_mac:
        print(f"[+] MAC address was successfully changed to {_current}")
    else:
        print("[+] MAC address was not changed.")


def main():
    """Main program engine"""
    options = get_arguments()
    # Save initial MAC address (not required)
    old_mac = get_mac(options.shell, options.interface)
    change_mac(options.shell, options.interface, options.new_mac)
    check_change(options.shell, options.interface, options.new_mac)

    # delete the following if you do not want to change back mac address
    change_mac(options.shell, options.interface, old_mac)
    print(f"current MAC address: {get_mac(options.shell, options.interface)}")


if __name__ == "__main__":
    main()
