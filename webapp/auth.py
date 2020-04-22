""" Authentication of a local activation."""
from flask import jsonify
import os
import sys

def check(ip_address, mac_list):
    """ Check the IP for being within the local network. """

    if '192.168.1' in ip_address:
        mac = get_mac(ip_address)
        if mac in mac_list:
            return True
        else:
            print("Mac address not found:")
            print(mac)
            return False
    else:
        return False

def get_mac(ip_address):
    arp_string = os.popen('arp -a | grep ' + ip_address).read()
    if ip_address in arp_string:
        left, arp_string = arp_string.split('at ', 1)
        if 'on' in arp_string:
            mac, right = arp_string.split(' [ether]', 1)
            mac = mac.strip()
            return mac
        return None
    return None
