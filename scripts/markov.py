#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Code by Julian Metzler aka Mezgrman

"""
Script to generate text on a basic Markov model
"""

import random

class Markov(object):
	"""
	The class to analyze and generate text
	"""
	
	def __init__(self, group_size = 3):
		assert group_size >= 2
		self.group_size = group_size
		self.cache = {}
	
	def create_cache(self, text):
		words = text.split()
		groups = self.generate_groups(words)
		self.cache = {}
		
		for group in groups:
			key = group[:self.group_size - 1]
			value = group[-1]
			
			if key in self.cache:
				self.cache[key].append(value)
			else:
				self.cache[key] = [value]
	
	def generate_groups(self, words):
		assert len(words) >= self.group_size
		
		for i in range(len(words) - (self.group_size - 1)):
			group = [words[i]]
			
			for n in range(self.group_size - 1):
				group.append(words[i + n + 1])
			
			yield tuple(group)
	
	def generate_text(self, max_length = 25):
		assert max_length > 0
		start_group = random.choice(self.cache.keys())
		result = list(start_group)
		
		while len(result) < max_length:
			group = tuple(result[1 - self.group_size:])
			try:
				word = random.choice(self.cache[group])
			except KeyError:
				break
			result.append(word)
		
		return " ".join(result)
	
	def generate_formatted_text(self, max_length = 25):
		text = self.generate_text(max_length)
		words = text.split()
		words[0] = words[0].capitalize()
		
		if words[-1][-1] not in ".!?":
			punctuation = random.choice([".", "!", "?"])
			words[-1] += punctuation
		
		text = " ".join(words)
		return text

if __name__ == "__main__":
	main()