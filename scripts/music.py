#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

"""
This script plays music using the `beep` command. Example file structure:

120
8F4 8D4 8A3 8D4 8F4 8D4 8A3 8D4
8F4 8C4 8A3 8C4 8F4 8C4 8A3 8C4
8E4 8C#4 8A3 8C#4 8E4 8C#4 8A3 8C#4 8E4 8C#4 8A3 8C#4 8E4 8C#4 8A3 8C#4

2.D4 4E4 1F4 4.A4 4.G4 4A4 1C4
2.D4 4E4 2F4 2E4 2G4 2A4 2G4 2F4
4P 4F4 4F4 4F4 4A4 4A4 4G4 4F4 4P 4A4 4A4 4A4 4G4 4A4 4G4 4F4
4P 4F4 4F4 4F4 4A4 4A4 4G4 4F4 4P 4A4 4A4 4A4 4P 4C#5 4C#5 4C#5
4P 4F4 4F4 4F4 4A4 4A4 4G4 4F4 4P 4Bb4 4Bb4 4Bb4 2G4 2C5
2A4 2C#5 8D3 8A3 8E3 8D4 8A3 8F4 8D4 8A4 8D5 8P 4P 2P

Play around with it and you will see how it works.
"""

import sys
import os
import re

FIXED_FREQ = 440.0
FIXED_NOTE = "A"
FIXED_NOTE_OCTAVE = 4
FIXED_NOTE_MOD = 0
NOTE_SEQ = "C|D|EF|G|A|B"
DURATION_MULTIPLIER = 15
DEFAULT_DURATION = 1.0 / 4.0
DEFAULT_OCTAVE = 4
DEFAULT_SPEED = 120
DEFAULT_LOOPS = 1
MULTIPLE_BEEP_CALLS = False
DEBUG = False

def beep(frequencies = [440.0], durations = [200.0]):
	diff = len(frequencies) - len(durations)
	if(diff > 0):
		for i in range(diff):
			durations.append(200.0)
	elif(diff < 0):
		for i in range(abs(diff)):
			frequencies.append(440.0)
	args = []
	for i in range(len(frequencies)):
		args.append("-f %f -l %f" % (frequencies[i], durations[i]))
	cmd = "beep %s" % " -n ".join(args)
	if(DEBUG):
		print "Command: %s" % cmd
	return os.system(cmd)

def parse_notes(string):
	notes = string.split()
	note_list = []
	pattern = re.compile(r"^(?P<dur>\d{0,2})(?P<ext>\.{0,1})(?P<note>[A-GP]{1})(?P<mod>[b#]{0,1})(?P<octave>\d{0,1})(?P<staccato>S{0,1})$")
	try:
		speed = int(notes[0])
	except:
		speed = DEFAULT_SPEED
	try:
		loops = int(notes[1])
	except:
		loops = DEFAULT_LOOPS
	for note in notes:
		match = pattern.match(note)
		if(match is not None):
			dur = 1.0 / float(match.group("dur")) if match.group("dur") != "" and match.group("dur") != "0" else DEFAULT_DURATION
			dur = dur * 1.5 if match.group("ext") != "" else dur
			tone = match.group("note")
			octave = int(match.group("octave")) + 1 if match.group("octave") != "" and match.group("octave") != "0" else DEFAULT_OCTAVE
			if(match.group("mod") == "b"):
				mod = -1
			elif(match.group("mod") == "#"):
				mod = 1
			else:
				mod = 0
			if match.group("staccato") == "S":
				note_list.append((dur * 0.5, tone, octave, mod))
				note_list.append((dur * 0.5, "P", octave, 0))
			else:
				note_list.append((dur, tone, octave, mod))
	return speed, loops, note_list

def calculate_absolute_pos(note, octave, mod):
	pos = NOTE_SEQ.find(note) + ((octave - 1) * len(NOTE_SEQ)) + mod
	return pos

def calculate_dist_from_a(note, octave, mod):
	absolute_pos = calculate_absolute_pos(note, octave, mod)
	fixed_pos = calculate_absolute_pos(FIXED_NOTE, FIXED_NOTE_OCTAVE, FIXED_NOTE_MOD)
	dist = absolute_pos - fixed_pos
	return dist

def calculate_freq(note, octave, mod):
	if(note == "P"):
		freq = 1.0
	else:
		freq = FIXED_FREQ * ((2 ** (1.0 / 12.0)) ** calculate_dist_from_a(note, octave, mod))
	return freq

def main():
	def newline_replace(match):
		return "\n%s " % match.group(0).strip()
	
	print "Running as process #%i" % os.getpid()
	try:
		with open(os.path.join(os.getcwdu(), sys.argv[1])) as f:
			raw_notes = re.sub(r" \d+ ", newline_replace, f.read().replace("\n", " ")).splitlines()
			print raw_notes
	except:
		raw_notes = [raw_input("Notes: ")]
	for line in raw_notes:
		speed, loops, notes = parse_notes(line)
		n = 0
		while(n < loops):
			if(not MULTIPLE_BEEP_CALLS):
				frequencies = []
				durations = []
			for note in notes:
				frequency = calculate_freq(note[1], note[2], note[3])
				duration = (note[0] * DURATION_MULTIPLIER * (10000 / speed))
				if(DEBUG):
					print "=" * 25 + "\nDuration:     %.3f\nNote:         %s\nOctave:       %i\nModification: %i\nFrequency:    %.3f Hz" % (duration, note[1], note[2], note[3], frequency)
				if(MULTIPLE_BEEP_CALLS):
					beep([frequency], [duration])
				else:
					frequencies.append(frequency)
					durations.append(duration)
			if(not MULTIPLE_BEEP_CALLS):
				beep(frequencies, durations)
			n += 1

try:
	main()
except KeyboardInterrupt:
	print
	sys.exit()
