#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2014 Julian Metzler

"""
Script to get station codes for German train stations and vice versa
"""

import argparse
import sqlite3

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--station', type = str, help = "A station name or code to look up")
	parser.add_argument('-db', '--database', type = str, default = "db_stations.db", help = "The database file to use")
	args = parser.parse_args()
	
	db = sqlite3.connect(args.database)
	cur = db.cursor()
	
	cur.execute("SELECT * FROM `stations` WHERE `code` = ? OR `name` LIKE ?", (args.station, "%" + args.station + "%"))
	matches = cur.fetchall()
	
	print "Found %i stations." % len(matches)
	
	for code, name in matches:
		print "%s\t%s" % (code, name)
	
	cur.close()
	db.close()

if __name__ == "__main__":
	main()