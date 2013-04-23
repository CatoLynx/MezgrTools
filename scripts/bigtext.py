#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

"""
This script displays large text on the screen. Should be self-explaining.
"""

import argparse
import datetime
import sys
import time
from string import Template

CHARMAP = {
'0': "\
██████████\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██████████",
	'1': "\
      ████\n\
        ██\n\
        ██\n\
        ██\n\
        ██\n\
        ██\n\
        ██",
	'2': "\
██████████\n\
        ██\n\
        ██\n\
██████████\n\
██        \n\
██        \n\
██████████",
	'3': "\
██████████\n\
        ██\n\
        ██\n\
    ██████\n\
        ██\n\
        ██\n\
██████████",
	'4': "\
██      ██\n\
██      ██\n\
██      ██\n\
██████████\n\
        ██\n\
        ██\n\
        ██",
	'5': "\
██████████\n\
██        \n\
██        \n\
██████████\n\
        ██\n\
        ██\n\
██████████",
	'6': "\
██████████\n\
██        \n\
██        \n\
██████████\n\
██      ██\n\
██      ██\n\
██████████",
	'7': "\
██████████\n\
        ██\n\
        ██\n\
      ██  \n\
    ██    \n\
  ██      \n\
  ██      ",
	'8': "\
██████████\n\
██      ██\n\
██      ██\n\
██████████\n\
██      ██\n\
██      ██\n\
██████████",
	'9': "\
██████████\n\
██      ██\n\
██      ██\n\
██████████\n\
        ██\n\
        ██\n\
██████████",
	'A': "\
██████████\n\
██      ██\n\
██      ██\n\
██████████\n\
██      ██\n\
██      ██\n\
██      ██",
	'B': "\
████████  \n\
██      ██\n\
██      ██\n\
████████  \n\
██      ██\n\
██      ██\n\
████████  ",
	'C': "\
██████████\n\
██        \n\
██        \n\
██        \n\
██        \n\
██        \n\
██████████",
	'D': "\
████████  \n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
████████  ",
	'E': "\
██████████\n\
██        \n\
██        \n\
████████  \n\
██        \n\
██        \n\
██████████",
	'F': "\
██████████\n\
██        \n\
██        \n\
████████  \n\
██        \n\
██        \n\
██        ",
	'G': "\
██████████\n\
██        \n\
██        \n\
██████████\n\
██      ██\n\
██      ██\n\
██████████",
	'H': "\
██      ██\n\
██      ██\n\
██      ██\n\
██████████\n\
██      ██\n\
██      ██\n\
██      ██",
	'I': "\
██████\n\
  ██  \n\
  ██  \n\
  ██  \n\
  ██  \n\
  ██  \n\
██████",
	'J': "\
██████████\n\
        ██\n\
        ██\n\
        ██\n\
██      ██\n\
██      ██\n\
██████████",
	'K': "\
██      ██\n\
██    ██  \n\
██  ██    \n\
████      \n\
██  ██    \n\
██    ██  \n\
██      ██",
	'L': "\
██        \n\
██        \n\
██        \n\
██        \n\
██        \n\
██        \n\
██████████",
	'M': "\
██      ██\n\
████  ████\n\
██  ██  ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██",
	'N': "\
██      ██\n\
███     ██\n\
██ █    ██\n\
██  ██  ██\n\
██    █ ██\n\
██     ███\n\
██      ██",
	'O': "\
██████████\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██████████",
	'P': "\
██████████\n\
██      ██\n\
██      ██\n\
██████████\n\
██        \n\
██        \n\
██        ",
	'Q': "\
██████████\n\
██      ██\n\
██      ██\n\
██      ██\n\
██    █ ██\n\
██     ███\n\
██████████",
	'R': "\
██████████\n\
██      ██\n\
██      ██\n\
██████████\n\
██  ██    \n\
██    ██  \n\
██      ██",
	'S': "\
██████████\n\
██        \n\
██        \n\
██████████\n\
        ██\n\
        ██\n\
██████████",
	'T': "\
██████████\n\
    ██    \n\
    ██    \n\
    ██    \n\
    ██    \n\
    ██    \n\
    ██    ",
	'U': "\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██████████",
	'V': "\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
 ██    ██ \n\
  ██  ██  \n\
    ██    ",
	'W': "\
██      ██\n\
██      ██\n\
██      ██\n\
██      ██\n\
██  ██  ██\n\
████  ████\n\
██      ██",
	'X': "\
██      ██\n\
 ██    ██ \n\
  ██  ██  \n\
    ██    \n\
  ██  ██  \n\
 ██    ██ \n\
██      ██",
	'Y': "\
██      ██\n\
 ██    ██ \n\
  ██  ██  \n\
    ██    \n\
    ██    \n\
    ██    \n\
    ██    ",
	'Z': "\
██████████\n\
       ██ \n\
      ██  \n\
    ██    \n\
  ██      \n\
 ██       \n\
██████████",
	':': "\
  \n\
██\n\
  \n\
  \n\
  \n\
██\n\
  ",
	'.': "\
  \n\
  \n\
  \n\
  \n\
  \n\
  \n\
██",
	'?': "\
██████████\n\
        ██\n\
        ██\n\
    ██████\n\
    ██    \n\
          \n\
    ██    ",
	'!': "\
██\n\
██\n\
██\n\
██\n\
██\n\
  \n\
██",
	';': "\
  \n\
██\n\
  \n\
  \n\
 █\n\
█ \n\
  ",
	',': "\
  \n\
  \n\
  \n\
  \n\
  \n\
 █\n\
█ ",
	' ': "\
        \n\
        \n\
        \n\
        \n\
        \n\
        \n\
        ",
	'(': "\
  ██\n\
██  \n\
██  \n\
██  \n\
██  \n\
██  \n\
  ██",
	')': "\
██  \n\
  ██\n\
  ██\n\
  ██\n\
  ██\n\
  ██\n\
██  ",
	'~': "\
          \n\
          \n\
  ██      \n\
██  ██  ██\n\
      ██  \n\
          \n\
          ",
	'=': "\
          \n\
          \n\
██████████\n\
          \n\
██████████\n\
          \n\
          ",
	'"': "\
█ █\n\
█ █\n\
   \n\
   \n\
   \n\
   \n\
   ",
	'§': "\
  █████ \n\
██     █\n\
 █████  \n\
██    ██\n\
  █████ \n\
█     ██\n\
 █████  ",
	'$': "\
    ██    \n\
██████████\n\
██  ██    \n\
██████████\n\
    ██  ██\n\
██████████\n\
    ██    ",
	'%': "\
███     ██\n\
█ █    ██ \n\
███   ██  \n\
    ██    \n\
  ██   ███\n\
 ██    █ █\n\
██     ███",
	'&': "\
   ████   \n\
  █    █  \n\
   ████   \n\
    ██  █ \n\
  ██  ██  \n\
 █    ███ \n\
  ████  ██",
	'/': "\
        ██\n\
       ██ \n\
      ██  \n\
    ██    \n\
  ██      \n\
 ██       \n\
██        ",
	'\\': "\
██        \n\
 ██       \n\
  ██      \n\
    ██    \n\
      ██  \n\
       ██ \n\
        ██",
	'[': "\
████\n\
██  \n\
██  \n\
██  \n\
██  \n\
██  \n\
████",
	']': "\
████\n\
  ██\n\
  ██\n\
  ██\n\
  ██\n\
  ██\n\
████",
	'{': "\
  ██\n\
 ██ \n\
 ██ \n\
██  \n\
 ██ \n\
 ██ \n\
  ██",
	'}': "\
██  \n\
 ██ \n\
 ██ \n\
  ██\n\
 ██ \n\
 ██ \n\
██  ",
	'\'': "\
█\n\
█\n\
 \n\
 \n\
 \n\
 \n\
 ",
	'█': "\
  ██  ██  \n\
  ██  ██  \n\
██████████\n\
  ██  ██  \n\
██████████\n\
  ██  ██  \n\
  ██  ██  ",
	'|': "\
██\n\
██\n\
██\n\
██\n\
██\n\
██\n\
██",
	'>': "\
██      \n\
  ██    \n\
    ██  \n\
      ██\n\
    ██  \n\
  ██    \n\
██      ",
	'<': "\
      ██\n\
    ██  \n\
  ██    \n\
██      \n\
  ██    \n\
    ██  \n\
      ██",
	'-': "\
        \n\
        \n\
        \n\
████████\n\
        \n\
        \n\
        ",
}

class DeltaTemplate(Template):
	delimiter = "%"

def get_terminal_size():
	import fcntl, os, struct, termios
	for i in range(10):
		try:
			size = struct.unpack('hh', fcntl.ioctl(i, termios.TIOCGWINSZ, '1234'))
		except:
			continue
		else:
			break
	return size # (height, width)

def multiline_join(blocks, align, width, separator = ""):
	lines = []
	n = 0
	for block in blocks:
		block_lines = block.splitlines()
		for i in range(len(block_lines)):
			try:
				lines[i] += block_lines[i]
			except IndexError:
				lines.append(block_lines[i])
			if(n < len(blocks) - 1):
				lines[i] += separator
		n += 1
	if align == 'right':
		lines = [line.decode('utf-8').rjust(width) for line in lines]
	elif align == 'center':
		lines = [line.decode('utf-8').center(width) for line in lines]
	else:
		lines = [line.decode('utf-8').ljust(width) for line in lines]
	result = "\n".join(lines)
	return result

def big_text(text, halign, valign, width, height, separator = "  "):
	blocks = []
	for char in text:
		try:
			blocks.append(CHARMAP[char])
		except KeyError:
			try:
				blocks.append(CHARMAP[char.upper()])
			except KeyError:
				pass
	result = multiline_join(blocks, halign, width, separator = separator)
	text_height = len(result.splitlines())
	remaining_height = height - text_height
	if valign == 'top':
		result += "\n" * remaining_height
	elif valign == 'middle':
		result = "\n" * (remaining_height / 2) + result + "\n" * (remaining_height / 2)
	elif valign == 'bottom':
		result = "\n" * remaining_height + result
	else:
		pass
	return result

def gen_countdown(target, fmt, display_fmt):
	now = datetime.datetime.now()
	target = datetime.datetime.strptime(target, fmt)
	delta = target - now
	seconds = delta.total_seconds()
	microseconds = seconds - int(seconds)
	seconds = int(seconds)
	minutes, seconds = divmod(seconds, 60.0)
	hours, minutes = divmod(minutes, 60.0)
	days, hours = divmod(hours, 24.0)
	years, days = divmod(days, 365.0)
	years, days, hours, minutes, seconds = [int(number) for number in (years, days, hours, minutes, seconds)]
	
	total_days = days + years * 365
	total_hours = hours + total_days * 24
	total_minutes = minutes + total_hours * 60
	total_seconds = seconds + total_minutes * 60
	
	t = DeltaTemplate(display_fmt)
	formatted_delta = t.substitute(Y = years, D = days, H = "%02i" % hours, M = "%02i" % minutes, S = "%02i" % seconds, U = microseconds, TD = total_days, TH = total_hours, TM = total_minutes, TS = total_seconds)
	return formatted_delta

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--text', default = "Hello world!")
	parser.add_argument('-ha', '--horizontal-align', choices = ['left', 'center', 'right'], default = 'left')
	parser.add_argument('-va', '--vertical-align', choices = ['top', 'middle', 'bottom', 'none'], default = 'none')
	parser.add_argument('-m', '--mode', choices = ['text', 'clock', 'countdown'], default = 'text')
	parser.add_argument('-cf', '--clock-format', default = "%H:%M:%S")
	parser.add_argument('-ta', '--target', default = "")
	parser.add_argument('-tf', '--target-format', default = "%d.%m.%Y %H:%M:%S")
	parser.add_argument('-cdf', '--countdown-format', default = "%H:%M:%S")
	args = parser.parse_args()
	
	height, width = get_terminal_size()
	
	if args.mode == 'text':
		if sys.stdin.isatty():
			text = args.text
		else:
			text = sys.stdin.read()
		print big_text(text, halign = args.horizontal_align, valign = args.vertical_align, width = width, height = height)
	elif args.mode == 'clock':
		while True:
			print big_text(time.strftime(args.clock_format), halign = args.horizontal_align, valign = args.vertical_align, width = width, height = height)
			time.sleep(1)
	elif args.mode == 'countdown':
		while True:
			print big_text(gen_countdown(args.target, args.target_format, args.countdown_format), halign = args.horizontal_align, valign = args.vertical_align, width = width, height = height)
			time.sleep(1)

if __name__ == "__main__":
	get_terminal_size()
	sys.stdout.write("\033[?25l")
	try:
		main()
	finally:
		sys.stdout.write("\033[?25h")