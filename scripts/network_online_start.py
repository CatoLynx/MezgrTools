#!/usr/bin/env python3
# Copyright 2015 Julian Metzler

"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This script checks whether at least one of several hosts in a local network is online
and if so, sends a Wake-On-LAN packet to a host in the local network.
"""

import os
import time
import yaml
from wakeonlan import wol

CONFIGFILE = "network_online_start.conf"

def check_hosts(hosts):
    for host in hosts:
        offline = bool(os.system('ping -c 1 %s >/dev/null 2>&1' % host))
        if not offline:
            # At least one host is online
            return True
    # All hosts are offline
    return False

def main():
    # Load the configuration
    with open(CONFIGFILE, 'r') as f:
        config = yaml.load(f.read())

    # Check if the target host is already running
    print("Checking if target is already online...")
    target_online = check_hosts([config['target_ip']])
    if target_online:
        print("Target is already online, exiting.")
        return

    # Check if any hosts are online
    print("Checking hosts...")
    online = check_hosts(config['ip_addresses'])
    if not online:
        print("No hosts online, exiting.")
        return

    # At least one host is online, send the WOL packet
    print("Sending WOL packet to %s..." % config['target_mac'])
    wol.send_magic_packet(config['target_mac'])


if __name__ == "__main__":
    main()