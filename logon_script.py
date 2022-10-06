import os
import sys
import subprocess
from subprocess import Popen, PIPE
from datetime import datetime
from zoneinfo import ZoneInfo
import pprint
from local_net_utilities import who_am_i, test_dns_resolution, get_default_gateway, get_time

session_logging = [
    get_time(timezone='America/Chicago'),
    who_am_i(),
    get_default_gateway(),
    test_dns_resolution(url='www.archlinux.org')
]
for entry in session_logging:
    for key, val in entry.items():
        print(f"{key} :: {val}")
script_call = subprocess.Popen(
    ['vpn_diag.sh'],stdout=PIPE,
    stderr=PIPE,
    universal_newlines=True,
    shell=True)

with script_call.stdout:
    for line in script_call.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
