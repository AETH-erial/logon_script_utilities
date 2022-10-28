import os
import sys
import subprocess
import time
from subprocess import Popen, PIPE
from datetime import datetime
from zoneinfo import ZoneInfo
import pprint
from local_net_utilities import (who_am_i,
                                test_dns_resolution,
                                get_default_gateway,
                                get_time,
                                get_external_ip,
                                get_dns_server,
                                resolve_ip_to_fqdn)
from console_colors import ConsoleColors


session_logging = [
    get_time(timezone='America/Chicago'),
    who_am_i(),
    get_default_gateway(),
    get_external_ip(),
    get_dns_server(),
    test_dns_resolution(url='www.archlinux.org')
]
for dns_servers in get_dns_server():
    session_logging.append(resolve_ip_to_fqdn(dns_servers))


script_call = subprocess.Popen(
    ['vpn_diag.sh'],stdout=PIPE,
    stderr=PIPE,
    universal_newlines=True,
    shell=True)

with script_call.stdout:
    for line in script_call.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()


for entry in session_logging:
    for key, val in entry.items():
        print(f"{ConsoleColors.UNDERLINE}{key}{ConsoleColors.ENDC} :: {ConsoleColors.OKGREEN}{val}{ConsoleColors.ENDC}")
        time.sleep(.5)
input(f"{ConsoleColors.OKGREEN}Press Enter to continue...{ConsoleColors.ENDC}")