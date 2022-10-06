import ipaddress
import socket
import sys
import struct
from datetime import datetime
from zoneinfo import ZoneInfo


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
            test_result = {'default_gateway': def_gateway}
            return test_result

def test_dns_resolution(url: str) -> str:
    """Method to test if DNS resolves or not.

    :type url: string
    :param url: the address to be resolved against DNS
    
    :rtype: bool
    :returns: True or False based on if DNS is resolving or not.
    """
    try:
        str_dns_addr = socket.gethostbyname(url)
        dns_test_address = ipaddress.IPv4Address(str_dns_addr)
        test_result = {url: dns_test_address}
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

def get_time(timezone: str) -> datetime:
    """Method to get the time that the script is ran/log in time.
    
    :type timezone: string
    :param timezone: the timezone to create the timestamp in

    :rtype: datetime
    :returns: the datetime object of the script execution.
    """
    right_now = datetime.now(tz=ZoneInfo(f'{timezone}'))
    timestamp = {'current time': right_now}
    return timestamp


