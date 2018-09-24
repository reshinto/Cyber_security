#!/usr/bin/env python3

import subprocess  # required to run shell commands


# disable ethernet_interface if it exist
subprocess.call("ifconfig eth0 down", shell=True)
# change ethernet_interface's mac address
subprocess.call("ifconfig eth0 hw ether 00:11:22:33:44:55", shell=True)
# enable ethernet_interface
subprocess.call("ifconfig eth0 up, shell=True)


