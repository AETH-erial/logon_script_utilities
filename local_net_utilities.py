import ipaddress
from ipaddress import IPv4Address
import socket
import sys
import struct
import subprocess
from subprocess import Popen, PIPE
from urllib.request import urlopen, HTTPError
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
            def_gateway = IPv4Address(socket.inet_ntoa(struct.pack("<L", int(fields[2], 16))))
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
        dns_test_address = IPv4Address(str_dns_addr)
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


def get_external_ip() -> IPv4Address:
    """Get the external facing IP address of the network.
    
    :type: None
    :param: None
    
    :rtype: IPv4Address
    :returns: IPv4Address class object of the external IP.
    """
    try:
        with urlopen('https://ident.me') as response:
            external_ip = response.read().decode('ascii')
        test_result = {'External IP Address': external_ip}
        return test_result
    except urllib.error as error:
        raise Exception(f'There was an issue getting your external IP. {error}')


def is_valid_address(address: str) -> bool:
    """checks to see if the address passed converts to bytes.
    
    :type address: str
    :param address: the address to be tested
    
    :rtype: bool
    :returns: true if the address is in valid format.
    
    :raises AttributeError: if the address is non-parseable.
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError as error:
        raise AttributeError(f'Address was non-parseable. Raising from is_valid_address{error}')
    return True

def get_dns_server() -> IPv4Address:
    """Get the IP address of the DNS server you are using.
    
    :type: None
    :param: None
    
    :rtype: IPv4Address
    :returns: An IPv4Address class object of your DNS Server's address.
    """
    dns_servers = []
    test_results = {}
    with open('/etc/resolv.conf') as fp:
        for num, line in enumerate(fp):
            columns = line.split()
            if columns[0] == 'nameserver':
                dns_entry = columns[1]
                if is_valid_address(dns_entry) == True:
                    dns_servers.append(dns_entry)
    test_results['dns servers'] = dns_servers
    return test_results

def resolve_ip_to_fqdn(address: str) -> str:
    """Resolve an IP address to an FQDN.
    
    :type address: str
    :param address: the address to be resolved.
    
    :rtype: str
    :returns: the FQDN of the address that was resolved.
    
    :raises Exception: if IP couldn't resolve to a hostname.
    """
    command_output = []
    parsed_output = []
    script_call = subprocess.Popen(
                            ['dig',
                            '+noall',
                            '+authority',
                            '-x',
                            f'{address}'],
                            stdout=PIPE,
                            stderr=PIPE
                            )
    with script_call.stdout:
        for output in script_call.stdout:
            entry = output.decode('utf-8')
            command_output.append(entry)
        parsed_output = command_output[0].split()
        SOA = parsed_output[0]
    test_result = {
        'SOA': f'{SOA}'
    }
    return test_result