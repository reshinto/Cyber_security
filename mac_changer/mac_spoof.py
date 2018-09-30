#!/usr/bin/env python3
"""
MAC address spoofer. Currently works in Kali linux, may work for Ubuntu.
Code works for Mac OSX, but not functioning as it should.
TODO: implement windows ipconfig command
"""
import subprocess  # required to run shell commands
import argparse  # required for getting user input from args
import re


def get_arguments():
    """
    Run and input the following:
    python mac-changer.py -s ifconfig -i eth0 -m 00:11:22:33:44:55
    then return the argument values
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shell", dest="shell",
                        help="shell command for ip address (eg. ifconfig)")
    parser.add_argument("-i", "--interface", dest="interface",
                        help="Interface to change MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac",
                        help="New MAC address")
    _args = parser.parse_args()
    if not _args.shell:
        parser.error("[-] Please specify a shell command, "
                     "use --help for more info")
    elif not _args.interface:
        parser.error("[-] Please specify an interface, "
                     "use --help for more info")
    elif not _args.new_mac:
        parser.error("[-] Please specify a new MAC address, "
                     "use --help for more info")
    return _args


def change_mac(shell, interface, new_mac, kali=False):
    """
    shell = ifconfig
    Disable interface -> change MAC address -> enable interface
    """
    print(f"[+] Changing MAC address for {interface}")
    subprocess.call([shell, interface, "down"])
    _change_mac(shell, interface, new_mac, kali)
    subprocess.call([shell, interface, "up"])


def _change_mac(shell, interface, new_mac, kali=False):
    """
    Check if hw is required
    hw is required for Kali linux
    """
    if kali is False:
        subprocess.call([shell, interface, "ether", new_mac])
    else:
        subprocess.call([shell, interface, "hw", "ether", new_mac])


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
    args = get_arguments()
    # Save initial MAC address (not required)
    old_mac = get_mac(args.shell, args.interface)
    change_mac(args.shell, args.interface, args.new_mac)
    check_change(args.shell, args.interface, args.new_mac)

    # delete the following if you do not want to change back mac address
    change_mac(args.shell, args.interface, old_mac)
    print(f"current MAC address: {get_mac(args.shell, args.interface)}")


if __name__ == "__main__":
    main()
