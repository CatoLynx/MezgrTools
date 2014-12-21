#!/usr/bin/env python3
# coding: utf-8
# Script by Julian Metzler

"""
Script to randomly mix up .wav files
"""

import random
import sys
import wave

def main():
	w = wave.open(sys.argv[1], 'rb')
	raw_data = w.readframes(w.getnframes())
	mix_data = []
	
	cur_pos = 0
	data_length = len(raw_data)
	while cur_pos < data_length:
		print("%i / %i" % (cur_pos, data_length))
		length = random.randint(10000, 100000)
		if length % 2 != 0:
			length += 1
		mix_data.append(raw_data[cur_pos:cur_pos + length])
		cur_pos += length
	
	random.shuffle(mix_data)
	
	o = wave.open(sys.argv[2], 'wb')
	o.setnchannels(w.getnchannels())
	o.setsampwidth(w.getsampwidth())
	o.setframerate(w.getframerate())
	o.writeframes(b"".join(mix_data))

if __name__ == "__main__":
	main()