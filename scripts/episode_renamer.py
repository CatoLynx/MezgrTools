#!/usr/bin/python
# -*- coding: utf-8 -*-
# Tool to auto-detect season and episode numbers from filenames and rename the files.
# © 2012 Mezgrman

import re
import os
import sys
import random

TEST_MODE = False
TEST_FILENAME = "4x06 This. No, really~ This.Is_A-fucking-ugly-name.so.let's.make_it_more_readable-Name.720p.x264....avi"

WORD_FILTER = [
	"144p",
	"240p",
	"360p",
	"480p",
	"720p",
	"1080p",
	"HDTV",
	"x264",
]

patterns = [
r"(?i)(?P<name>.+?)\s*[\(\[\{]{1}\s*S\s*(?P<season>\d+)[\W\s]*E\s*(?P<episode>\d+)(?P<part>\w{0,1})\s*[\}\]\)]\s*\.(?P<container>\w+)$", # Name (S2E09b).ext
r"(?i)(?P<name>.+?)\s*[\(\[\{]{1}\s*Season\s*(?P<season>\d+)[\W\s]*Episode\s*(?P<episode>\d+)(?P<part>\w{0,1})\s*[\}\]\)]\s*\.(?P<container>\w+)$", # Name [Season 2, Episode 9b].ext
r"(?i)(?P<name>.+?)\s*[\(\[\{]{1}\s*(?P<season>\d+)\s*[xX]{1}\s*(?P<episode>\d+)(?P<part>\w{0,1})\s*[\}\]\)]\s*\.(?P<container>\w+)$", # Name {2x09b}.ext
r"(?i).*Season\s*(?P<season>\d+)[\W\s]*Episode\s*(?P<episode>\d+)(?P<part>\w{0,1})[\W\s]*(?P<name>.+?)\s*\.(?P<container>\w+)$", # Show Name Season 2 – Episode 9b: Name.ext
r"(?i).*S\s*(?P<season>\d+)[\W\s]*E\s*(?P<episode>\d+)(?P<part>\w{0,1})[\W\s]*(?P<name>.+?)\s*\.(?P<container>\w+)$", # Some irrelevant text here S 2 E 9b – Name.ext
r"(?i).*(?P<season>\d+)\s*[xX]{1}\s*(?P<episode>\d+)(?P<part>\w{0,1})[\W\s]*(?P<name>.+?)\s*\.(?P<container>\w+)$", # 2x09b Name.ext
r"(?i).*?(?P<season>\d{1,2}?)\s*(?P<episode>\d{1,2})(?P<part>\w{0,1})[\W\s]*(?P<name>.+?)\s*\.(?P<container>\w+)$" # Show name 209b Name.ext
]
containers = ["mp4", "flv", "mpg", "mpeg", "webm", "avi", "srt", "sub", "3gp", "m4v", "mov", "qt", "divx", "vob", "evo", "mkv", "asf", "wmv", "rm", "rmvb", "ogv"]

def get_data(filename):
	match = False
	for pattern in patterns:
		match = re.match(pattern, filename)
		if(match):
			break
	
	if not match:
		return False
	
	name = re.sub(r"\s*\[.*\]", "", match.group('name'))
	name = name.replace("_", "#") # Temporarily replace underscores with hashes to make the regex easier
	name = re.sub(r"\b[.\-#]\b", " ", name) # Convert This.Is_An-Episode.Name to This Is An Episode Name
	name = name.replace("#", "_") # Change the remaining hashes back to underscores.
	
	for word in WORD_FILTER:
		name = re.sub(r"(?i)%s" % word, "", name)
	
	name = " ".join(name.split()) # Convert multiple spaces to one
	
	if(match):
		return (int(match.group('season')), int(match.group('episode')), match.group('part'), name, match.group('container').lower())
	else:
		return False

def main():
	if(TEST_MODE):
		data = get_data(TEST_FILENAME)
		if(data):
			season, episode, part, name, container = data
			print "Filename:  %s\nSeason:    %i\nEpisode:   %i\nPart:      %s\nName:      %s\nContainer: %s" % (TEST_FILENAME, season, episode, part, name, container)
		else:
			print "No match!"
		sys.exit()
	
	try:
		path = sys.argv[1]
	except:
		path = os.getcwdu()
	
	if(path[-1:] != "/"):
		path += "/"
	
	print "Scanning %s..." % path,
	
	used_files = []
	files = os.listdir(path)
	for filename in files:
		container = filename.split('.')
		container = container[len(container) - 1]
		if((not os.path.isdir(path + filename)) and container in containers and get_data(filename)):
			used_files.append(filename)
	
	if(len(used_files) > 0):
		print "%i files found." % len(used_files)
	else:
		print "No files found."
		sys.exit()
	
	while(True):
		action = raw_input("What would you like to do?\n\nList files [L]\nRename files [R]\nCancel [C]\nYour choice: ").upper()
		if(action == "C"):
			print "Canceled."
			sys.exit()
		elif(action == "L"):
			print "=" * 100
			for filename in used_files:
				print filename
			print "=" * 100
		elif(action == "R"):
			break
	
	while(True):
		while(True):
			scheme = raw_input("Please enter the new name scheme for the files without the file extension. Required placeholders:\n\n{S} or {0S} - The season number of the episode ({0S} with a leading zero)\n{E} or {0E} - The number of the episode in the season ({0E} with a leading zero)\n{N} - The name of the episode\n\n\nOptional placeholders:\n\n{P} - The part of the episode\n\nScheme: ")
			if(scheme != "" and ("{S}" in scheme.upper() or "{0S}" in scheme.upper()) and ("{E}" in scheme.upper() or "{0E}" in scheme.upper()) and "{N}" in scheme.upper()):
				break
		
		scheme = re.sub(r"(?i)\{S\}", "%(season)i", scheme)
		scheme = re.sub(r"(?i)\{0S\}", "%(season)02i", scheme)
		scheme = re.sub(r"(?i)\{E\}", "%(episode)i", scheme)
		scheme = re.sub(r"(?i)\{0E\}", "%(episode)02i", scheme)
		scheme = re.sub(r"(?i)\{P\}", "%(part)s", scheme)
		scheme = re.sub(r"(?i)\{N\}", "%(name)s", scheme)
		scheme += ".%(container)s"
		season, episode, part, name, container = get_data(random.choice(used_files))
		example_name = scheme.decode('utf-8') % {'season': season, 'episode': episode, 'part': part, 'name': name, 'container': container}
		confirm = raw_input(u"Here is an example filename according to your name scheme:\n\n%s\n\nIs this OK? [Y/N]: " % example_name).upper()
		if(confirm == "Y"):
			break
	
	print "OK. Renaming files..."
	
	success_count = 0
	failure_count = 0
	for filename in used_files:
		season, episode, part, name, container = get_data(filename)
		new_filename = scheme.decode('utf-8') % {'season': season, 'episode': episode, 'part': part, 'name': name, 'container': container}
		if(not os.path.exists(path + new_filename)):
			try:
				os.rename(path + filename, path + new_filename)
			except OSError:
				print "Failed to rename %." % filename
				failure_count += 1
			else:
				success_count += 1
		else:
			print u"Failed to rename %s: Destination file %s already exists." % (filename, new_filename)
			failure_count += 1
	
	print "%i files successfully renamed, %i errors." % (success_count, failure_count)

main()
