#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2014 Julian Metzler

"""
IBIS (VDV 300) bus utility for various devices
"""

import serial

class IBISMaster(object):
	def __init__(self, port):
		self.port = port
		self.device = serial.serial_for_url(
			self.port,
			baudrate = 1200,
			bytesize = serial.SEVENBITS,
			parity = serial.PARITY_EVEN,
			stopbits = serial.STOPBITS_TWO
		)
	
	def hash(self, message):
		check_byte = 0x7F
		
		for char in message:
			byte = ord(char)
			check_byte = check_byte ^ byte
		
		message += chr(check_byte)
		return message
	
	def send_raw(self, data):
		print repr(data)
		hex_data = ""
		for byte in data:
			hex_data += "<%s>" % hex(ord(byte))[2:].upper().rjust(2, "0")
		print hex_data
		return self.device.write(data)
	
	def send_message(self, message):
		message = message.replace("ä", "{")
		message = message.replace("ö", "|")
		message = message.replace("ü", "}")
		message = message.replace("ß", "~")
		message = message.replace("Ä", "[")
		message = message.replace("Ö", "\\")
		message = message.replace("Ü", "]")
		message = self.hash(message + "\r")
		return self.send_raw(message)
	
	def send_line_number(self, line_number):
		message = "l%03i" % line_number
		return self.send_message(message)
	
	def send_special_character(self, character):
		message = "lE%02i" % character
		return self.send_message(message)
	
	def send_target_number(self, target_number):
		message = "z%03i" % target_number
		return self.send_message(message)
	
	def send_time(self, hours, minutes):
		message = "u%02i%02i" % (hours, minutes)
		return self.send_message(message)
	
	def send_date(self, day, month, year):
		message = "d%02i%02i%i" % (day, month, year)
		return self.send_message(message)
	
	def send_target_text__003a(self, text):
		blocks, remainder = divmod(len(text), 16)
		
		if remainder:
			blocks += 1
			text += " " * (16 - remainder)
		
		message = "zA%i%s" % (blocks, text.upper())
		return self.send_message(message)
	
	def send_target_text__021(self, text, id):
		blocks, remainder = divmod(len(text), 16)
		
		if remainder:
			blocks += 1
			text += " " * (16 - remainder)
		
		message = "aA%i%i%s" % (id, blocks, text.upper())
		return self.send_message(message)
	
	def send_next_stop__009(self, next_stop, length = 16):
		message = "v%s" % next_stop.upper().ljust(length)
		return self.send_message(message)
	
	def send_next_stop__003c(self, next_stop):
		blocks, remainder = divmod(len(next_stop), 4)
		
		if remainder:
			blocks += 1
			next_stop += " " * (4 - remainder)
		
		message = "zI%i%s" % (blocks, next_stop)
		return self.send_message(message)

def main():
	import time
	master = IBISMaster("/dev/ttyUSB0")
	while True:
		master.send_next_stop__003c(time.strftime("%d.%m.%Y %H:%M"))
		time.sleep(60)

if __name__ == "__main__":
	main()