#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

"""
This script takes a sentence and breaks it up into the largest possible repeating patterns.
"""

from collections import Counter
from pprint import pprint
import argparse
import re
import sys

def _slices(string, size):
	for i in range(len(string) - size + 1):
		yield string[i:i + size]

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--text', default = "Hello world!")
	args = parser.parse_args()
	
	if sys.stdin.isatty():
		text = args.text
	else:
		text = sys.stdin.read()
	
	length = len(text)
	_patterns = []
	for n in range(1, length + 1):
		slices = []
		for s in _slices(text, n):
			slices.append(s)
		_patterns.append(slices)
	
	patterns = []
	for slices in _patterns:
		c = Counter(slices)
		patterns += [(item, count) for item, count in c.iteritems() if count > 1]
	
	_patterns = patterns[:]
	patterns = []
	for i in range(len(_patterns) - 1, -1, -1):
		item, count = _patterns[i]
		occurences = len(re.findall(re.escape(item), text))
		if occurences > 1:
			patterns.append((item, occurences))
	
	results = []
	for i in range(len(patterns)):
		for n in range(len(patterns)):
			if n == i:
				continue
			if patterns[i] is None or patterns[n] is None:
				continue
			if patterns[n][0] in patterns[i][0]:
				patterns[n] = None
	
	while None in patterns:
		patterns.remove(None)
	
	max_length = max([len(item) for item, count in patterns])
	for item, count in patterns:
		print item + " " * (max_length + 2 - len(item)) + str(count)

if __name__ == "__main__":
	main()