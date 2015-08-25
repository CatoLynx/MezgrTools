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
and if not, shuts down the computer, but only at certain times of the day.

This script needs to be run as root in order to shutdown the system.
"""

import datetime
import os
import time
import yaml

CONFIGFILE = "network_offline_shutdown.conf"

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
    start_time = datetime.datetime.strptime(config['start_time'], "%H-%M").time()
    end_time = datetime.datetime.strptime(config['end_time'], "%H-%M").time()

    # Check the time to see if we're in the right time of day
    print("Checking time...")
    current_time = datetime.datetime.now().time()
    if (start_time < end_time and (current_time < start_time or current_time > end_time)) or (start_time > end_time and (current_time < start_time and current_time > end_time)):
        print("Not the right time, exiting.")
        return

    # We are in the right timespan, check if any hosts are online
    print("Checking hosts...")
    online = check_hosts(config['ip_addresses'])
    if online:
        print("At least one host online, exiting.")
        return

    # No hosts were online at this point, wait the specified amount of time and re-check
    # (e.g. in case one host was rebooting at the time of the check)
    print("No hosts online, waiting %i seconds..." % config['confirmation_time'])
    time.sleep(config['confirmation_time'])
    print("Checking hosts...")
    online = check_hosts(config['ip_addresses'])
    if online:
        print("At least one host online, exiting.")
        return

    # Definitely no hosts are online and we can shutdown
    print("No hosts online, shutting down.")
    os.system('shutdown now -h >/dev/null 2>&1')


if __name__ == "__main__":
    main()