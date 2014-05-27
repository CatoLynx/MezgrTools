#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2014 Julian Metzler

"""
Script to shift an entire file by a specified number of bits
"""

import argparse
import os
import sys

def main():
	parser = argparse.ArgumentParser(description = "Shift an entire file by a specified number of bits")
	parser.add_argument('-n', '--number', default = 1, type = int, help = "How many bits to shift")
	parser.add_argument('-f', '--file', required = True, type = str, help = "The file to shift")
	parser.add_argument('-o', '--output', required = True, type = str, help = "The file to store the shifted data in")
	parser.add_argument('-v', '--verbose', action = 'store_true', help = "Verbose output")
	args = parser.parse_args()
	
	if args.verbose:
		sys.stdout.write("Loading file...")
		sys.stdout.flush()
	
	with open(args.file, 'rb') as f:
		data = f.read()
	
	size = os.path.getsize(args.file)
	
	if args.verbose:
		sys.stdout.write(" %i bytes\n" % size)
		sys.stdout.flush()
	
	if args.verbose:
		sys.stdout.write("Converting file content to binary string...")
		sys.stdout.flush()
	
	bin_data = ""
	for byte in data:
		bin_data += bin(ord(byte))[2:].rjust(8, "0")
	
	bin_size = len(bin_data)
	
	if args.verbose:
		sys.stdout.write(" %i bits\n" % bin_size)
		sys.stdout.flush()
	
	number = args.number % bin_size
	
	if number == 0:
		sys.stdout.write("No shifting necessary, aborting.\n")
		sys.exit(0)
	
	if args.verbose:
		sys.stdout.write("Shifting binary string by %i bits...\n" % number)
		sys.stdout.flush()
	
	bin_data = bin_data[-number:] + bin_data[:bin_size - number]
	
	if args.verbose:
		sys.stdout.write(" Done\n")
		sys.stdout.flush()
	
	if args.verbose:
		sys.stdout.write("Converting binary string back to file...")
		sys.stdout.flush()
	
	new_data = ""
	for bin_byte in (bin_data[pos:pos + 8] for pos in xrange(0, bin_size, 8)):
		byte = chr(int(bin_byte, 2))
		new_data += byte
	
	new_size = len(new_data)
	
	if args.verbose:
		sys.stdout.write(" %i bytes\n" % new_size)
		sys.stdout.flush()
	
	if args.verbose:
		sys.stdout.write("Saving file...")
		sys.stdout.flush()
	
	with open(args.output, 'wb') as f:
		f.write(bytearray(new_data))
	
	if args.verbose:
		sys.stdout.write(" Done\n")

if __name__ == "__main__":
	main()