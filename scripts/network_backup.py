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
This script starts a remote host, mounts samba shares on that host, syncs them with local directories, unmounts the shares and shuts down the remote host.
"""

import os
import sys
import yaml
from wakeonlan import wol

CONFIGFILE = "network_backup.conf"

def check_host_online(host):
    return not bool(os.system('ping -c 1 %s >/dev/null 2>&1' % host))

def main():
    # Load the configuration
    with open(CONFIGFILE, 'r') as f:
        config = yaml.load(f.read())

    # Check if host is already online
    print("Checking if remote is already online...")
    if not check_host_online(config['remote_ip']):
        print("Remote is offline. Sending WOL packet to %s..." % config['remote_mac'])
        wol.send_magic_packet(config['remote_mac'])

        # Wait until host is reachable
        print("Waiting until remote is online...")
        while not check_host_online(config['remote_ip']):
            pass

    # Remote is online, prepare the backup process
    print("Starting backup.")
    print("Creating mountpoint %s..." % config['mountpoint'])
    try:
        os.mkdir(config['mountpoint'])
    except OSError as exc:
        print("FATAL: Failed to create mountpoint %s: %s" % (config['mountpoint'], str(exc)), file = sys.stderr)
        return

    # Do the backup
    for share in config['shares']:
        # Mount the share
        print("Mounting samba share //%s/%s on %s..." % (config['remote_ip'], share['name'], config['mountpoint']))
        fail = bool(os.system("mount -t cifs //%s/%s %s -o username=%s,password=%s,domain=%s" % (
            config['remote_ip'],
            share['name'],
            config['mountpoint'],
            share['username'],
            share['password'],
            share['domain'])))
        if fail:
            print("FATAL: Failed to mount //%s/%s on %s." % (config['remote_ip'], share['name'], config['mountpoint']), file = sys.stderr)
            return

        # Run rsync
        print("Backing up %s to //%s/%s..." % (share['source'], config['remote_ip'], share['name']))
        fail = bool(os.system("rsync -a -h --no-o --no-g --delete --progress %s %s" % (share['source'], config['mountpoint'])))
        if fail:
            print("WARNING: Backup of %s to //%s/%s failed or was incomplete." % (share['source'], config['remote_ip'], share['name']), file = sys.stderr)

        # Unmount the share
        print("Unmounting //%s/%s from %s..." % (config['remote_ip'], share['name'], config['mountpoint']))
        fail = bool(os.system("umount %s" % config['mountpoint']))
        if fail:
            print("FATAL: Failed to unmount //%s/%s from %s." % (config['remote_ip'], share['name'], config['mountpoint']), file = sys.stderr)
            return

    # Backup done, remove mountpoint
    print("Removing mountpoint %s..." % config['mountpoint'])
    try:
        os.rmdir(config['mountpoint'])
    except OSError as exc:
        print("FATAL: Failed to remove mountpoint %s: %s" % (config['mountpoint'], str(exc)), file = sys.stderr)
        return


if __name__ == "__main__":
    main()