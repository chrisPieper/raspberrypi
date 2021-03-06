""" Authentication of a local activation."""
import os


def check(range, ip_address, mac_list, logger):
    " Check the IP for being within the local network. "

    if range in ip_address:
        mac = get_mac(ip_address)
        if mac in mac_list:
            return True
        else:
            logger.warning(f'MAC address not found: {mac}')
            return False
    else:
        return False


def get_mac(ip_address):
    " Strip the mac (hardware) address from the result of 'arp'. "

    arp_string = os.popen('arp -a | grep ' + ip_address).read()
    if ip_address in arp_string:
        _, arp_string = arp_string.split('at ', 1)
        if 'on' in arp_string:
            mac, _ = arp_string.split(' [ether]', 1)
            mac = mac.strip()
            return mac
        return None
    return None
