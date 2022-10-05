import ipaddress
import socket
import sys
import struct


##  method to get the default gateway of your machine
def get_default_gateway() -> str:
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
            def_gateway = ipaddress.IPv4Address(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
            test_result = f"""
            Your machine appears to have a default gateway.
            Address: {def_gateway}"""
            return test_result

def test_dns_resolution(url: str) -> str:
    """Method to test if DNS resolves or not.
    
    :rtype: bool
    :returns: True or False based on if DNS is resolving or not.
    """
    try:
        str_dns_addr = socket.gethostbyname(url)
        dns_test_address = ipaddress.IPv4Address(str_dns_addr)
        test_result = f"""
            DNS resolution deemed successful.
            '{url}' resolved to: {dns_test_address}"""
        return test_result
    except socket.error as error:
        raise Exception(f'Exception raised when attempting DNS resolution {error}') from error
    
def who_am_i() -> str:
    """Method to return the address and hostname of the box.
    
    :rtype: str
    :returns: hostname and local address
    """
    local_host = socket.gethostname()
    hostname_resolution = socket.gethostbyname(local_host)
    test_result = {local_host: hostname_resolution}
    return test_result
