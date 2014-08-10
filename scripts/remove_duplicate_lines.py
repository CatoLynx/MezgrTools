#!/usr/bin/env python
# (C) 2014 Julian Metzler

import sys

def main():
	filename = sys.argv[1]
	
	with open(filename, 'r+') as f:
		lines = [line.strip("\n") for line in f.readlines()]
		f.seek(0)
		f.truncate()
		f.write("\n".join(set(lines)))

if __name__ == "__main__":
	main()