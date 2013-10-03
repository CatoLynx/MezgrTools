#!/usr/bin/python
# -*- coding: utf-8 -*-
# (C) 2013 Julian Metzler

"""
A VERY VERY BASIC, but flexible and easily customizable text-to-speech engine
NOT AT ALL suited for long texts because it is very disk space intensive and absolutely not efficiently coded

Just record wave files and name them what you recorded. Recommended basic setup is the letters of your language plus a few common diphtongs that are
pronounced differently than just the letters themselves.

Example basic files for German would be a.wav, b.wav, c.wav, ..., z.wav, ä.wav, ö.wav, ü.wav, ß.wav, sch.wav, ch.wav and so on.
"""

import argparse
import os
from subprocess import check_output as shell

def main():
	# Initialize the command-line argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--text', default = "Hello world!", help = "The text to speak")
	parser.add_argument('-c', '--case-sensitive', action = 'store_true', default = False, help = "Case-sentitive reading")
	parser.add_argument('-v', '--voice', default = "speech-data", help = "The speech sample directory to use")
	parser.add_argument('-o', '--outfile', default = None, help = "The output file to write the wave data to")
	args = parser.parse_args()
	
	# Load available samples (IMPORTANT: Use lowercase file extensions)
	speech_samples = [fname[:-4] for fname in os.listdir(args.voice) if fname.endswith(".wav")]
	speech_samples.sort(key = len, reverse = True)
	text = args.text.replace("\0", "")
	used_samples = {}
	
	# Prepare the text
	if not args.case_sensitive:
		text = text.lower()
	 
	# Split the text into the largest possible chunks
	for sample in speech_samples:
		while (args.case_sensitive and sample in text) or (not args.case_sensitive and sample.lower() in text):
			pos = text.find(sample)
			used_samples[pos] = sample
			text = text.replace(sample, "\0" * len(sample), 1)
			# print text, used_samples
	
	# Generate the list of samples to play
	ordered_samples = [item[1] for item in sorted(used_samples.items(), key = lambda entry: entry[0])]
	
	# Setup the names for temporary data
	tmpdir = "/tmp/awesomespeechsynthesis"
	outfile = args.outfile if args.outfile else os.path.join(tmpdir, 'out.wav')
	
	# Remove temporary directory if it already exists
	shell(('rm', '-rf', tmpdir))
	
	# Copy the used sample files to a temporary directory
	try:
		os.mkdir(tmpdir)
	except:
		pass
	
	for index, sample in enumerate(ordered_samples):
		name = "/tmp/awesomespeechsynthesis/%05i.wav" % index
		shell(('cp', os.path.join(args.voice, sample + ".wav"), name))
	
	# Concatenate the samples into a single wave file
	shell(('sox', os.path.join(tmpdir, '*.wav'), outfile))
	
	# Play the result
	shell(('aplay', outfile))
	

if __name__ == "__main__":
	main()