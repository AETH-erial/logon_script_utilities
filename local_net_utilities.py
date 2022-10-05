import ipaddress
import socket
import sys
import struct


##  method to get the default gateway of your machine
def get_default_gateway():
    """Method to get the default gateway of your machine.
    Linux/Unix based method.
    
    :rtype: ipaddress
    :returns: the ip address of your default gateway.
    """
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return ipaddress.IPv4Address(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))

def test_dns_resolution(url: str, port: int) -> bool:
    """Method to test if DNS resolves or not.
    
    :rtype: bool
    :returns: True or False based on if DNS is resolving or not.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host_ip = socket.gethostbyname(url)
    except socket.error as err:
        raise Exception(f'Exception raised when attempting DNS resolution {err}') from err
        sys.exit()
    sock.connect((host_ip, port))

    
    
test_dns_resolution(url='www.google.com', port=80)
