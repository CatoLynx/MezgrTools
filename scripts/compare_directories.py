#!/usr/bin/python
# -*- coding: utf-8 -*-
# (C) 2014 Julian Metzler

"""
Compare directories and list files present in only one directory but not the other
I use it to check if my cloud photo upload really uploaded everything before deleting photos
"""

import argparse
import os
import shutil

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d1', '--dir-1', help = "First directory for the comparison")
	parser.add_argument('-d2', '--dir-2', help = "Second directory for the comparison")
	parser.add_argument('-a', '--action',
		choices = ('print', 'copy-to-1', 'copy-to-2', 'move-to-1', 'move-to-2'),
		default = 'print',
		help = "What to do with the files that have been found")
	args = parser.parse_args()
	
	files_1 = os.listdir(args.dir_1)
	files_2 = os.listdir(args.dir_2)
	
	files_only_in_1 = [f for f in files_1 if f not in files_2]
	files_only_in_2 = [f for f in files_2 if f not in files_1]
	
	if args.action == 'print':
		print "Files present only in %s:\n%s\n" % (args.dir_1, "\n".join(files_only_in_1))
		print "Files present only in %s:\n%s" % (args.dir_2, "\n".join(files_only_in_2))
	elif args.action == 'copy-to-1':
		print "Copying files that are present only in %s to %s..." % (args.dir_2, args.dir_1)
		n = len(files_only_in_2)
		i = 1
		for f in files_only_in_2:
			print "[%i / %i] Copying %s..." % (i, n, f)
			shutil.copy(os.path.join(args.dir_2, f), args.dir_1)
			i += 1
	elif args.action == 'copy-to-2':
		print "Copying files that are present only in %s to %s..." % (args.dir_1, args.dir_2)
		n = len(files_only_in_1)
		i = 1
		for f in files_only_in_1:
			print "[%i / %i] Copying %s..." % (i, n, f)
			shutil.copy(os.path.join(args.dir_1, f), args.dir_2)
			i += 1
	elif args.action == 'move-to-1':
		print "Moving files that are present only in %s to %s..." % (args.dir_2, args.dir_1)
		n = len(files_only_in_2)
		i = 1
		for f in files_only_in_2:
			print "[%i / %i] Moving %s..." % (i, n, f)
			shutil.move(os.path.join(args.dir_2, f), args.dir_1)
			i += 1
	elif args.action == 'move-to-2':
		print "Moving files that are present only in %s to %s..." % (args.dir_1, args.dir_2)
		n = len(files_only_in_1)
		i = 1
		for f in files_only_in_1:
			print "[%i / %i] Moving %s..." % (i, n, f)
			shutil.move(os.path.join(args.dir_1, f), args.dir_2)
			i += 1

if __name__ == "__main__":
	main()