import sys
import socket

import nmap
import bluetooth

from jarbas_house.devices import GenericDevice


# Get your local network IP address. e.g. 192.168.178.X
def get_lan_ip():
    try:
        return ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in
                 [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    except socket.error as e:
        sys.stderr.write(str(e) + "\n")  # probably offline / no internet connection
        sys.exit(e.errno)


# Scan you local network for all hosts
def scan_wifi(nmap_args="-sn"):
    hosts = str(".".join(get_lan_ip().split(".")[:-1])) + ".0/24"
    scanner = nmap.PortScanner()
    scanner.scan(hosts=hosts, arguments=nmap_args)

    for ip in scanner.all_hosts():
        name = scanner[ip].hostname()
        yield GenericDevice(ip, name, scanner[ip])


def scan_bluetooth():
    for addr, name in bluetooth.discover_devices(lookup_names=True):
        yield GenericDevice(addr, name, {"address": addr, "name": name, "device_type": "bluetooth"})


if __name__ == "__main__":
    from pprint import pprint
    for host in scan_wifi():
        pprint(host.as_dict)
    for host in scan_bluetooth():
        pprint(host.as_dict)
