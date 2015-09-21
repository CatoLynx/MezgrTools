#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# © 2015 Julian Metzler

"""
This script seaches for duplicate files in a givn folder using their checksums
and removes any duplicates it encounters.
"""

import argparse
import hashlib
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description = "Duplicate file remover")
    parser.add_argument('-d', '--dir', required = True,
        help = "The directory in which to look for duplicate files")
    parser.add_argument('-t', '--trash-dir',
        help = "The directory to move the duplicate files to. If omitted, they will be deleted.")
    args = parser.parse_args()
    
    print("Scanning directory...")
    all_files = os.listdir(args.dir)
    print("    %i files found." % len(all_files))

    print("Generating MD5 hashes of all files...")
    hashes = {}

    for filename in all_files:
        fullname = os.path.join(args.dir, filename)
        if not os.path.isfile(fullname):
            continue
        print("    Hashing %s..." % filename, end = " ")
        filehash = hashlib.md5(open(fullname, 'rb').read()).hexdigest()
        print(filehash)
        if filehash in hashes:
            hashes[filehash].append(filename)
        else:
            hashes[filehash] = [filename]

    print("Checking for duplicate hashes...")
    for hash, files in hashes.items():
        if len(files) < 2:
            continue

        print("    Found %i possible duplicates with hash %s:" % (len(files), hash))
        print("\n".join(["        " + filename for filename in files]))
        shortest_name = sorted(files, key = lambda name: len(name))[0]
        print("            Keeping %s" % shortest_name)

        files.remove(shortest_name)

        for filename in files:
            if args.trash_dir:
                shutil.move(os.path.join(args.dir, filename), os.path.join(args.trash_dir, filename))
            else:
                os.remove(os.path.join(args.dir, filename))

if __name__ == "__main__":
    main()