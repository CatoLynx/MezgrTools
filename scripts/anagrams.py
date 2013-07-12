#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2013 Mezgrman

"""
Script to find anagrams using a database of words
"""

import argparse
import random
import sqlite3

def get_char_stats(word, case_sensitive = True):
	stats = {}
	
	for char in word:
		if not case_sensitive:
			char = char.lower()
		
		if char in stats:
			stats[char] += 1
		else:
			stats[char] = 1
	
	return stats

def main():
	parser = argparse.ArgumentParser(description = "Anagram finder")
	parser.add_argument('-a', '--action', choices = ('find', 'build'), default = 'find', help = "Find anagrams or build the word database")
	parser.add_argument('-wf', '--word-file', default = "/usr/share/dict/words", help = "The word list (one word per line) to build the database from")
	parser.add_argument('-db', '--database', default = "anagram_words.db", help = "The database file to use")
	parser.add_argument('-w', '--word', type = lambda s: s.decode('utf-8'), help = "The word to find anagrams for")
	parser.add_argument('-cs', '--case-sensitive', action = 'store_true', help = "Match case-sensitive")
	args = parser.parse_args()
	
	db = sqlite3.connect(args.database)
	db.row_factory = sqlite3.Row
	cur = db.cursor()
	
	if args.action == 'build':
		cur.execute("DROP TABLE IF EXISTS `words`")
		cur.execute("CREATE TABLE `words` (`word` TEXT, `length` INT)")
		
		with open(args.word_file, 'r') as word_file:
			for word in word_file.readlines():
				word = word.decode('utf-8').strip("\n")
				cur.execute("INSERT INTO `words` (`word`, `length`) VALUES (?, ?)", (word, len(word)))
		
		db.commit()
		print "Database built."
	
	elif args.action == 'find':
		length = len(args.word)
		cur.execute("SELECT * FROM `words` WHERE `length` = ?", (length, ))
		rows = cur.fetchall()
		word_stats = get_char_stats(args.word, args.case_sensitive)
		candidates = []
		
		for word, length in rows:
			if args.case_sensitive:
				if word == args.word:
					continue
			else:
				if word.lower() == args.word.lower():
					continue
			
			candidate_stats = get_char_stats(word, args.case_sensitive)
			if candidate_stats == word_stats:
				candidates.append(word)
		
		print "\n".join(candidates)

if __name__ == "__main__":
	main()